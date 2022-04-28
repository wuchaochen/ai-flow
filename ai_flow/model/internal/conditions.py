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
from notification_service.event import EventKey, Event
from typing import List

from ai_flow.model.condition import Condition
from ai_flow.model.context import Context


class SingleEventCondition(Condition):

    def __init__(self,
                 expect_event: EventKey):
        super().__init__([expect_event])

    def is_met(self, event: Event, context: Context) -> bool:
        return True


class MeetAllCondition(Condition):

    def __init__(self, conditions: List[Condition]):
        events = []
        for c in conditions:
            events.extend(c.expect_events)
        super().__init__(expect_events=events)
        self.conditions = conditions

    def is_met(self, event: Event, context: Context) -> bool:
        for condition in self.conditions:
            if not condition.is_met(event, context):
                return False
        return True


class MeetAnyCondition(Condition):

    def __init__(self, conditions: List[Condition]):
        events = []
        for c in conditions:
            events.extend(c.expect_events)
        super().__init__(expect_events=events)
        self.conditions = conditions

    def is_met(self, event: Event, context: Context) -> bool:
        for condition in self.conditions:
            if condition.is_met(event, context):
                return True
        return False
