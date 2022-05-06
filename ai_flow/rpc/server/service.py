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
from notification_service.notification_client import NotificationClient

from ai_flow.rpc.protobuf import common_pb2, namespace_pb2, namespace_pb2_grpc, workflow_pb2, workflow_pb2_grpc, \
    schedule_pb2, schedule_pb2_grpc, execution_pb2, execution_pb2_grpc


class BaseService(object):
    def __init__(self, metadata_manager, notification_client: NotificationClient):
        self.metadata_manager = metadata_manager
        self.notification_client = notification_client


class NamespaceService(BaseService, namespace_pb2_grpc.NamespaceServiceServicer):

    def addNamespace(self, request, context):
        return super().addNamespace(request, context)

    def getNamespace(self, request, context):
        return super().getNamespace(request, context)

    def updateNamespace(self, request, context):
        return super().updateNamespace(request, context)

    def listNamespace(self, request, context):
        return super().listNamespace(request, context)

    def deleteNamespace(self, request, context):
        return super().deleteNamespace(request, context)


class WorkflowService(BaseService, workflow_pb2_grpc.WorkflowServiceServicer):
    def addWorkflow(self, request, context):
        return super().addWorkflow(request, context)

    def updateWorkflow(self, request, context):
        return super().updateWorkflow(request, context)

    def getWorkflow(self, request, context):
        return super().getWorkflow(request, context)

    def deleteWorkflow(self, request, context):
        return super().deleteWorkflow(request, context)

    def disableWorkflow(self, request, context):
        return super().disableWorkflow(request, context)

    def enableWorkflow(self, request, context):
        return super().enableWorkflow(request, context)

    def listWorkflows(self, request, context):
        return super().listWorkflows(request, context)


class WorkflowScheduleService(BaseService, schedule_pb2_grpc.WorkflowScheduleServiceServicer):
    def addSchedule(self, request, context):
        return super().addSchedule(request, context)

    def getSchedule(self, request, context):
        return super().getSchedule(request, context)

    def deleteSchedule(self, request, context):
        return super().deleteSchedule(request, context)

    def pauseSchedule(self, request, context):
        return super().pauseSchedule(request, context)

    def resumeSchedule(self, request, context):
        return super().resumeSchedule(request, context)

    def listSchedules(self, request, context):
        return super().listSchedules(request, context)


class WorkflowTriggerService(BaseService, schedule_pb2_grpc.WorkflowTriggerServiceServicer):
    def addTrigger(self, request, context):
        return super().addTrigger(request, context)

    def getTrigger(self, request, context):
        return super().getTrigger(request, context)

    def deleteTrigger(self, request, context):
        return super().deleteTrigger(request, context)

    def pauseTrigger(self, request, context):
        return super().pauseTrigger(request, context)

    def resumeTrigger(self, request, context):
        return super().resumeTrigger(request, context)

    def listTriggers(self, request, context):
        return super().listTriggers(request, context)


class WorkflowExecutionService(BaseService, execution_pb2_grpc.WorkflowExecutionServiceServicer):
    def getWorkflowExecution(self, request, context):
        return super().getWorkflowExecution(request, context)

    def deleteWorkflowExecution(self, request, context):
        return super().deleteWorkflowExecution(request, context)

    def listWorkflowExecutions(self, request, context):
        return super().listWorkflowExecutions(request, context)

    def startWorkflowExecution(self, request, context):
        return super().startWorkflowExecution(request, context)

    def stopWorkflowExecution(self, request, context):
        return super().stopWorkflowExecution(request, context)


class TaskExecutionService(BaseService, execution_pb2_grpc.WorkflowExecutionServiceServicer):
    def getWorkflowExecution(self, request, context):
        return super().getWorkflowExecution(request, context)

    def deleteWorkflowExecution(self, request, context):
        return super().deleteWorkflowExecution(request, context)

    def listWorkflowExecutions(self, request, context):
        return super().listWorkflowExecutions(request, context)

    def startWorkflowExecution(self, request, context):
        return super().startWorkflowExecution(request, context)

    def stopWorkflowExecution(self, request, context):
        return super().stopWorkflowExecution(request, context)