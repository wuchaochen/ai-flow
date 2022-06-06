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
import logging
import queue
import threading

from notification_service.notification_client import NotificationClient

from ai_flow.common.exception.exceptions import AIFlowDBException
from ai_flow.common.util.db_util.session import create_session
from ai_flow.metadata.metadata_manager import MetadataManager
from ai_flow.scheduler.rule_executor import RuleExecutor
from ai_flow.scheduler.rule_wrapper import WorkflowRuleWrapper
from ai_flow.scheduler.schedule_command import WorkflowExecutionStartCommand, WorkflowExecutionStopCommand, \
    WorkflowExecutionScheduleCommand
from ai_flow.scheduler.scheduling_event_processor import SchedulingEventProcessor
from ai_flow.scheduler.scheduling_unit import SchedulingUnit
from ai_flow.scheduler.workflow_executor import WorkflowExecutor


class Worker(threading.Thread):
    """Worker's responsibility is executing the scheduling unit."""

    def __init__(self,
                 max_queue_size: int = 20,
                 task_executor=None,
                 db_engine=None,
                 notification_client: NotificationClient = None):
        super().__init__()
        self.input_queue = queue.Queue(max_queue_size)
        self.task_executor = task_executor
        self.db_engine = db_engine
        self.notification_client = notification_client

    def add_unit(self, unit: SchedulingUnit):
        self.input_queue.put(unit)

    def _execute_workflow_execution_schedule_command(self, command: WorkflowExecutionScheduleCommand):
        for c in command.task_schedule_commands:
            self.task_executor.schedule_command(c)

    def run(self) -> None:
        with create_session(db_engine=self.db_engine) as session:
            metadata_manager = MetadataManager(session=session)
            scheduling_event_processor = SchedulingEventProcessor(metadata_manager=metadata_manager)
            workflow_executor = WorkflowExecutor(metadata_manager=metadata_manager)
            rule_executor = RuleExecutor(metadata_manager=metadata_manager)
            while True:
                try:
                    event, rule = self.input_queue.get()
                    if event is None:
                        break
                    schedule_command = None
                    if rule is None:
                        command = scheduling_event_processor.process(event=event)
                        metadata_manager.flush()
                        if isinstance(command, WorkflowExecutionStartCommand) \
                                or isinstance(command, WorkflowExecutionStopCommand):
                            schedule_command = workflow_executor.execute(command)
                            metadata_manager.flush()
                        elif isinstance(command, WorkflowExecutionScheduleCommand):
                            schedule_command = command
                        else:
                            schedule_command = None
                    else:
                        if isinstance(rule, WorkflowRuleWrapper):
                            cmd = rule_executor.execute_workflow_rule(event=event, rule=rule)
                            metadata_manager.flush()
                            if cmd is not None:
                                schedule_command = workflow_executor.execute(command)
                                metadata_manager.flush()
                        else:
                            schedule_command = rule_executor.execute_workflow_execution_rule(event=event, rule=rule)
                            metadata_manager.flush()
                    if schedule_command is not None:
                        self._execute_workflow_execution_schedule_command(command=schedule_command)
                    metadata_manager.commit()
                except Exception as e:
                    session.rollback()
                    logging.error("Can not handle event {}, exception {}".format(str(event), str(e)))
                finally:
                    self.input_queue.task_done()

    def stop(self):
        self.input_queue.put((None, None))
        self.join()
