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
#
import time
import unittest

import cloudpickle
from notification_service.event import EventKey, Event

from ai_flow.model.action import TaskAction
from ai_flow.model.condition import Condition
from ai_flow.model.context import Context
from ai_flow.model.execution_type import ExecutionType
from ai_flow.model.internal.events import StartWorkflowExecutionEvent, StartTaskExecutionEvent
from ai_flow.model.operator import Operator
from ai_flow.model.rule import WorkflowRule
from ai_flow.model.status import WorkflowStatus
from ai_flow.model.workflow import Workflow
from ai_flow.scheduler.dispatcher import Dispatcher
from ai_flow.scheduler.rule_extractor import RuleExtractor
from ai_flow.scheduler.rule_wrapper import WorkflowExecutionRuleWrapper
from ai_flow.scheduler.schedule_command import TaskScheduleCommand
from ai_flow.scheduler.worker import Worker
from tests.scheduler.test_utils import UnitTestWithNamespace


class MockTaskExecutor(object):
    def __init__(self):
        self.commands = []

    def schedule_command(self, command):
        self.commands.append(command)


class TrueCondition(Condition):
    def is_met(self, event: Event, context: Context) -> bool:
        return True


def wait_worker_done(worker: Worker):
    while worker.input_queue.unfinished_tasks > 0:
        time.sleep(0.1)


class TestWorker(UnitTestWithNamespace):
    def setUp(self) -> None:
        super().setUp()
        with Workflow(name='workflow') as workflow:
            op1 = Operator(name='op_1')
            op2 = Operator(name='op_2')
            op1.action_on_condition(action=TaskAction.START, condition=TrueCondition(expect_events=[
                EventKey(namespace='namespace',
                         name='event_1',
                         event_type='event_type',
                         sender='sender'
                         ),
            ]))

        self.workflow_meta = self.metadata_manager.add_workflow(namespace=self.namespace_name,
                                                                name=workflow.name,
                                                                content='',
                                                                workflow_object=cloudpickle.dumps(workflow))
        self.metadata_manager.flush()
        self.workflow_trigger \
            = self.metadata_manager.add_workflow_trigger(self.workflow_meta.id,
                                                         rule=cloudpickle.dumps(WorkflowRule(
                                                             condition=TrueCondition(expect_events=[
                                                                 EventKey(namespace='namespace',
                                                                          name='event_2',
                                                                          event_type='event_type',
                                                                          sender='sender'
                                                                          ),
                                                             ]))))
        self.metadata_manager.flush()
        self.snapshot_meta = self.metadata_manager.add_workflow_snapshot(
            workflow_id=self.workflow_meta.id,
            workflow_object=self.workflow_meta.workflow_object,
            uri='url',
            signature='')
        self.metadata_manager.commit()

    def test_worker(self):
        task_executor = MockTaskExecutor()
        rule_extractor = RuleExtractor(metadata_manager=self.metadata_manager)
        worker = Worker(task_executor=task_executor, db_engine=self.db_engine)
        worker.start()

        event: Event = StartWorkflowExecutionEvent(workflow_id=self.workflow_meta.id, snapshot_id=self.snapshot_meta.id)
        worker.add_unit((event, None))
        wait_worker_done(worker)
        self.assertEqual(1, len(task_executor.commands))
        self.assertTrue(isinstance(task_executor.commands[0], TaskScheduleCommand))
        self.assertEqual(TaskAction.START, task_executor.commands[0].action)
        wes = self.metadata_manager.list_workflow_executions(workflow_id=self.workflow_meta.id)
        self.assertEqual(1, len(wes))
        tes = self.metadata_manager.list_task_executions(workflow_execution_id=wes[0].id)
        self.assertEqual(1, len(tes))

        event = Event(event_key=EventKey(namespace='namespace',
                                         name='event_1',
                                         event_type='event_type',
                                         sender='sender'), message='')
        rules = rule_extractor.extract_workflow_execution_rules(event=event)
        worker.add_unit((event, rules[0]))
        wait_worker_done(worker)

        self.assertEqual(2, len(task_executor.commands))
        tes = self.metadata_manager.list_task_executions(workflow_execution_id=wes[0].id)
        self.assertEqual(2, len(tes))

        event = Event(event_key=EventKey(namespace='namespace',
                                         name='event_2',
                                         event_type='event_type',
                                         sender='sender'), message='')
        rules = rule_extractor.extract_workflow_rules(event=event)
        worker.add_unit((event, rules[0]))
        wait_worker_done(worker)
        self.assertEqual(3, len(task_executor.commands))
        wes = self.metadata_manager.list_workflow_executions(workflow_id=self.workflow_meta.id)
        self.assertEqual(2, len(wes))
        tes = self.metadata_manager.list_task_executions(workflow_execution_id=wes[1].id)
        self.assertEqual(1, len(tes))
        worker.stop()


if __name__ == '__main__':
    unittest.main()
