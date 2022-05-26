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
from typing import Optional, Union

import cloudpickle

from ai_flow.metadata.metadata_manager import MetadataManager
from ai_flow.model.action import TaskAction
from ai_flow.model.task_execution import TaskExecutionKey
from ai_flow.model.workflow import Workflow
from ai_flow.scheduler.schedule_command import WorkflowScheduleCommand, TaskScheduleCommand, \
    WorkflowExecutionScheduleCommand, WorkflowExecutionStopCommand


class WorkflowExecutor(object):
    def __init__(self, metadata_manager: MetadataManager):
        self.metadata_manager = metadata_manager

    def execute(self, schedule_cmd: Union[WorkflowScheduleCommand, WorkflowExecutionStopCommand]) \
            -> Optional[WorkflowExecutionScheduleCommand]:
        if isinstance(schedule_cmd, WorkflowScheduleCommand):
            workflow_execution_meta = self.metadata_manager.add_workflow_execution(workflow_id=schedule_cmd.workflow_id,
                                                                                   run_type=schedule_cmd.run_type.value,
                                                                                   snapshot_id=schedule_cmd.snapshot_id)
            # self.metadata_manager.session.flush()
            snapshot_meta = self.metadata_manager.get_workflow_snapshot(snapshot_id=schedule_cmd.snapshot_id)
            workflow: Workflow = cloudpickle.loads(snapshot_meta.workflow_object)
            task_schedule_commands = []
            for task_name in workflow.tasks.keys():
                if task_name not in workflow.rules:
                    task_execution_meta = self.metadata_manager.add_task_execution(
                        workflow_execution_id=workflow_execution_meta.id,
                        task_name=task_name)
                    task_cmd = TaskScheduleCommand(action=TaskAction.START,
                                                   new_task_execution=TaskExecutionKey(
                                                       workflow_execution_id=workflow_execution_meta.id,
                                                       task_name=task_name,
                                                       seq_num=task_execution_meta.sequence_number,
                                                   ))
                    task_schedule_commands.append(task_cmd)
            if len(task_schedule_commands) > 0:
                return WorkflowExecutionScheduleCommand(workflow_execution_id=workflow_execution_meta.id,
                                                        task_schedule_commands=task_schedule_commands)
            else:
                return None
        else:
            task_execution_metas = self.metadata_manager.list_task_executions(
                workflow_execution_id=schedule_cmd.workflow_execution_id)
            if task_execution_metas is not None:
                task_schedule_commands = []
                for task_execution in task_execution_metas:
                    task_cmd = TaskScheduleCommand(action=TaskAction.STOP,
                                                   current_task_execution=TaskExecutionKey(
                                                       workflow_execution_id=task_execution.workflow_execution_id,
                                                       task_name=task_execution.task_name,
                                                       seq_num=task_execution.sequence_number,
                                                   ))
                    task_schedule_commands.append(task_cmd)
                if len(task_schedule_commands) > 0:
                    return WorkflowExecutionScheduleCommand(workflow_execution_id=schedule_cmd.workflow_execution_id,
                                                            task_schedule_commands=task_schedule_commands)
                else:
                    return None
            else:
                return None
