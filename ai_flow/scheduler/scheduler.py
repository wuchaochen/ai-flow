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
from notification_service.event import Event
from notification_service.embedded_notification_client import EmbeddedNotificationClient
from ai_flow.common.util.db_util.session import create_sqlalchemy_engine, new_session
from ai_flow.metadata.metadata_manager import MetadataManager
from ai_flow.scheduler.dispatcher import Dispatcher
from ai_flow.scheduler.worker import Worker


class EventDrivenScheduler(object):
    def __init__(self,
                 db_uri: str,
                 notification_server_uri: str,
                 schedule_worker_num: int
                 ):
        self.db_engine = create_sqlalchemy_engine(db_uri=db_uri)
        self.session = new_session(db_engine=self.db_engine)
        self.task_executor = None
        self.notification_client = EmbeddedNotificationClient(server_uri=notification_server_uri,
                                                              namespace='scheduler',
                                                              sender='scheduler')
        self.workers = []
        for i in range(schedule_worker_num):
            self.workers.append(Worker(max_queue_size=20, db_engine=self.db_engine, task_executor=self.task_executor))
        self.dispatcher = Dispatcher(workers=self.workers, metadata_manager=MetadataManager(session=self.session))

    def trigger(self, event: Event):
        self.dispatcher.dispatch(event=event)

    def start(self):
        self.task_executor.start()
        for i in range(len(self.workers)):
            self.workers[i].setDaemon(True)
            self.workers[i].setName('schedule_worker_{}'.format(i))
            self.workers[i].start()

    def stop(self):
        self.session.close()
        self.task_executor.stop()
        for w in self.workers:
            w.stop()
