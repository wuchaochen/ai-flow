# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import cloudpickle
from notification_service.event import Event
from typing import Optional

from ai_flow.metadata.metadata_manager import MetadataManager
from ai_flow.metadata.util import workflow_execution_meta_to_workflow_execution
from ai_flow.model.action import TaskAction
from ai_flow.model.context import Context
from ai_flow.model.task_execution import TaskExecutionKey
from ai_flow.scheduler.rule_wrapper import WorkflowExecutionRuleWrapper, WorkflowRuleWrapper
from ai_flow.scheduler.runtime_context import WorkflowExecutionContextImpl, WorkflowContextImpl
from ai_flow.scheduler.schedule_command import TaskScheduleCommand, WorkflowExecutionScheduleCommand, \
    WorkflowScheduleCommand


class RuleExecutor(object):

    @staticmethod
    def execute_workflow_execution_rule(event: Event,
                                        rule: WorkflowExecutionRuleWrapper,
                                        metadata_manager: MetadataManager) \
            -> Optional[WorkflowExecutionScheduleCommand]:
        """
        Execute all rules in a workflow execution
        :param event: The event that triggers the rule.
        :param rule: A wrapper for all task rules in a workflow execution.
        :param metadata_manager: A metadata manager.
        """

        def build_context(workflow_execution_rule: WorkflowExecutionRuleWrapper) -> Context:
            workflow_execution_meta = metadata_manager.get_workflow_execution(
                workflow_execution_id=workflow_execution_rule.workflow_execution_id)
            workflow_meta = workflow_execution_meta.workflow
            we = workflow_execution_meta_to_workflow_execution(workflow_execution_meta)
            return WorkflowExecutionContextImpl(workflow=cloudpickle.loads(workflow_meta.workflow_object),
                                                workflow_execution=we,
                                                metadata_manager=metadata_manager)

        context = build_context(workflow_execution_rule=rule)
        results = []
        for task_rule_wrapper in rule.task_rule_wrappers:
            action = None
            for task_rule in task_rule_wrapper.rules:
                action = task_rule.trigger(event=event, context=context)
                if action is not None:
                    break
            seq_num = metadata_manager.get_latest_sequence_number(workflow_execution_id=rule.workflow_execution_id,
                                                                  task_name=task_rule_wrapper.task_name)
            current_task_execution = TaskExecutionKey(workflow_execution_id=rule.workflow_execution_id,
                                                      task_name=task_rule_wrapper.task_name,
                                                      seq_num=seq_num)
            new_task_execution = TaskExecutionKey(workflow_execution_id=rule.workflow_execution_id,
                                                  task_name=task_rule_wrapper.task_name,
                                                  seq_num=seq_num + 1)
            if action is not None:
                if TaskAction.START == action:
                    result = TaskScheduleCommand(action=action,
                                                 current_task_execution=None,
                                                 new_task_execution=new_task_execution)
                elif TaskAction.RESTART == action:
                    result = TaskScheduleCommand(action=action,
                                                 current_task_execution=current_task_execution,
                                                 new_task_execution=new_task_execution)
                else:
                    result = TaskScheduleCommand(action=action,
                                                 current_task_execution=current_task_execution)
                results.append(result)
        if len(results) > 0:
            return WorkflowExecutionScheduleCommand(workflow_execution_id=rule.workflow_execution_id,
                                                    task_schedule_results=results)
        else:
            return None

    @staticmethod
    def execute_workflow_rule(event: Event,
                              rule: WorkflowRuleWrapper,
                              metadata_manager: MetadataManager) -> Optional[WorkflowScheduleCommand]:
        """
        Execute all rules on a workflow
        :param event: The event that triggers the rule.
        :param rule: A wrapper for all workflow rules on a workflow.
        :param metadata_manager: A metadata manager.
        """

        def build_context(workflow_rule_wrapper: WorkflowRuleWrapper) -> Context:
            workflow_meta = metadata_manager.get_workflow_by_id(workflow_id=workflow_rule_wrapper.workflow_id)
            return WorkflowContextImpl(namespace=workflow_meta.namespace,
                                       workflow=cloudpickle.loads(workflow_meta.workflow_object),
                                       metadata_manager=metadata_manager)

        context = build_context(workflow_rule_wrapper=rule)
        flag = False
        for workflow_rule in rule.rules:
            if workflow_rule.trigger(event=event, context=context):
                flag = True
                break
        if flag:
            return WorkflowScheduleCommand(workflow_id=rule.workflow_id)
        else:
            return None
