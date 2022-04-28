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
import unittest

from notification_service.event import Event
from ai_flow.model.action import TaskAction
from ai_flow.model.condition import Condition
from ai_flow.model.context import Context
from ai_flow.model.operator import Operator
from ai_flow.model.workflow import Workflow


class MockOperator(Operator):
    pass


class MockCondition(Condition):
    def __init__(self):
        super().__init__([])

    def is_met(self, event: Event, context: Context) -> bool:
        pass


class TestWorkflow(unittest.TestCase):

    def test_create_workflow(self):

        with Workflow(name='workflow') as workflow:
            task_1 = MockOperator(name='task_1')
            task_2 = MockOperator(name='task_2')
            task_1.action_on_condition(TaskAction.START, MockCondition())
            task_1.action_on_condition(TaskAction.START, MockCondition())
            task_2.action_on_condition(TaskAction.START, MockCondition())
        self.assertEqual(2, len(workflow.tasks))
        self.assertEqual(2, len(workflow.rules['task_1']))
        self.assertEqual(1, len(workflow.rules['task_2']))


if __name__ == '__main__':
    unittest.main()
