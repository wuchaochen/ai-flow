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
from enum import Enum
from typing import Optional
import json
from notification_service.event import Event, EventKey, DEFAULT_NAMESPACE

from ai_flow.model.status import TaskStatus


class AIFlowEventType(object):
    """
    AIFlow internal event types.
    TASK_STATUS_CHANGED: Task instance running status changed type.
    """
    TASK_STATUS_CHANGED = 'TASK_STATUS_CHANGED'
    AI_FLOW_INNER_EVENT = 'AI_FLOW_INNER_EVENT'


class InnerEventType(str, Enum):
    START_WORKFLOW_EXECUTION = 'START_WORKFLOW_EXECUTION'
    STOP_WORKFLOW_EXECUTION = 'STOP_WORKFLOW_EXECUTION'
    START_TASK_EXECUTION = 'START_TASK_EXECUTION'
    STOP_TASK_EXECUTION = 'STOP_TASK_EXECUTION'
    RESTART_TASK_EXECUTION = 'RESTART_TASK_EXECUTION'
    PERIODIC_RUN_WORKFLOW = 'PERIODIC_RUN_WORKFLOW'
    PERIODIC_RUN_TASK = 'PERIODIC_RUN_TASK'


class EventContextConstant(object):
    NAMESPACE = 'namespace'
    WORKFLOW_NAME = 'workflow_name'
    WORKFLOW_ID = 'workflow_id'
    WORKFLOW_EXECUTION_ID = 'workflow_execution_id'
    TASK_NAME = 'task_name'
    TASK_EXECUTION_ID = 'task_execution_id'
    WORKFLOW_SCHEDULE_ID = 'workflow_schedule_id'
    WORKFLOW_SNAPSHOT_ID = 'workflow_snapshot_id'


class TaskStatusChangedEventKey(EventKey):
    """TaskStatusChangedEventKey represents an event of the task status changed."""
    def __init__(self,
                 workflow_name: str,
                 task_name: str,
                 namespace: str = DEFAULT_NAMESPACE):
        """
        :param workflow_name: The name of the workflow to which the task belongs.
        :param task_name: The task's name.
        :param namespace: The task's namespace.
        """
        super().__init__(namespace=namespace,
                         name=workflow_name,
                         event_type=AIFlowEventType.TASK_STATUS_CHANGED,
                         sender=task_name)


class TaskStatusChangedEvent(Event):
    """TaskStatusChangedEvent is an event of the task status changed."""
    def __init__(self,
                 workflow_name: str,
                 workflow_execution_id: int,
                 task_name: str,
                 status: TaskStatus,
                 namespace: str = DEFAULT_NAMESPACE):
        """
        :param workflow_name: The name of the workflow to which the task belongs.
        :param workflow_execution_id: Unique ID of WorkflowExecution.
        :param task_name: The task's name.
        :param status: The current status of the task.
        :param namespace: The task's namespace.
        """
        super().__init__(event_key=TaskStatusChangedEventKey(workflow_name=workflow_name,
                                                             task_name=task_name,
                                                             namespace=namespace),
                         message=status)
        self.context = json.dumps({EventContextConstant.WORKFLOW_EXECUTION_ID: workflow_execution_id})


class InnerEvent(Event):
    """"""
    def __init__(self, name, message):
        super().__init__(EventKey(namespace=None,
                                  sender=None,
                                  name=name,
                                  event_type=AIFlowEventType.AI_FLOW_INNER_EVENT),
                         message)


class StartWorkflowExecutionEvent(InnerEvent):
    def __init__(self, snapshot_id):
        super().__init__(InnerEventType.START_WORKFLOW_EXECUTION, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_SNAPSHOT_ID: snapshot_id})


class StopWorkflowExecutionEvent(InnerEvent):
    def __init__(self, workflow_execution_id: int):
        super().__init__(InnerEventType.STOP_WORKFLOW_EXECUTION, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_EXECUTION_ID: workflow_execution_id})


class StartTaskExecutionEvent(InnerEvent):
    def __init__(self, workflow_execution_id: int, task_name: str):
        super().__init__(InnerEventType.START_TASK_EXECUTION, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_EXECUTION_ID: workflow_execution_id,
                                   EventContextConstant.TASK_NAME: task_name})


class ReStartTaskExecutionEvent(InnerEvent):
    def __init__(self, workflow_execution_id: int, task_name: str):
        super().__init__(InnerEventType.RESTART_TASK_EXECUTION, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_EXECUTION_ID: workflow_execution_id,
                                   EventContextConstant.TASK_NAME: task_name})


class StopTaskExecutionEvent(InnerEvent):
    def __init__(self, task_execution_id: int):
        super().__init__(InnerEventType.STOP_TASK_EXECUTION, None)
        self.context = json.dumps({EventContextConstant.TASK_EXECUTION_ID: task_execution_id})


class PeriodicRunTaskEvent(InnerEvent):
    """PeriodicRunTaskEvent is an event of starting a task."""
    def __init__(self,
                 workflow_execution_id: int,
                 task_name: str):
        """
        :param workflow_execution_id: The unique id of the workflow execution.
        :param task_name: The name of the task.
        """
        super().__init__(InnerEventType.PERIODIC_RUN_TASK, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_EXECUTION_ID: workflow_execution_id,
                                   EventContextConstant.TASK_NAME: task_name})


class PeriodicRunWorkflowEvent(InnerEvent):
    """PeriodicRunWorkflowEvent is an event of starting a workflow."""
    def __init__(self,
                 schedule_id: int):
        """
        :param schedule_id: The unique id of workflow schedule.
        """
        super().__init__(InnerEventType.PERIODIC_RUN_WORKFLOW, None)
        self.context = json.dumps({EventContextConstant.WORKFLOW_SCHEDULE_ID: schedule_id})
