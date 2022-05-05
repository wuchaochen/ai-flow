#
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

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import common_pb2 as common__pb2
from . import workflow_pb2 as workflow__pb2


class WorkflowServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.addWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/addWorkflow',
                request_serializer=workflow__pb2.WorkflowProto.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.updateWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/updateWorkflow',
                request_serializer=workflow__pb2.UpdateWorkflowRequest.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.getWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/getWorkflow',
                request_serializer=workflow__pb2.WorkflowIdentifier.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.deleteWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/deleteWorkflow',
                request_serializer=workflow__pb2.WorkflowIdentifier.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.disableWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/disableWorkflow',
                request_serializer=workflow__pb2.WorkflowIdentifier.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.enableWorkflow = channel.unary_unary(
                '/ai_flow.WorkflowService/enableWorkflow',
                request_serializer=workflow__pb2.WorkflowIdentifier.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )
        self.listWorkflows = channel.unary_unary(
                '/ai_flow.WorkflowService/listWorkflows',
                request_serializer=workflow__pb2.ListWorkflowsRequest.SerializeToString,
                response_deserializer=common__pb2.Response.FromString,
                )


class WorkflowServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def addWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def updateWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def getWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deleteWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disableWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enableWorkflow(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def listWorkflows(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WorkflowServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'addWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.addWorkflow,
                    request_deserializer=workflow__pb2.WorkflowProto.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'updateWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.updateWorkflow,
                    request_deserializer=workflow__pb2.UpdateWorkflowRequest.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'getWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.getWorkflow,
                    request_deserializer=workflow__pb2.WorkflowIdentifier.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'deleteWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.deleteWorkflow,
                    request_deserializer=workflow__pb2.WorkflowIdentifier.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'disableWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.disableWorkflow,
                    request_deserializer=workflow__pb2.WorkflowIdentifier.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'enableWorkflow': grpc.unary_unary_rpc_method_handler(
                    servicer.enableWorkflow,
                    request_deserializer=workflow__pb2.WorkflowIdentifier.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
            'listWorkflows': grpc.unary_unary_rpc_method_handler(
                    servicer.listWorkflows,
                    request_deserializer=workflow__pb2.ListWorkflowsRequest.FromString,
                    response_serializer=common__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ai_flow.WorkflowService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WorkflowService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def addWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/addWorkflow',
            workflow__pb2.WorkflowProto.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def updateWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/updateWorkflow',
            workflow__pb2.UpdateWorkflowRequest.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def getWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/getWorkflow',
            workflow__pb2.WorkflowIdentifier.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deleteWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/deleteWorkflow',
            workflow__pb2.WorkflowIdentifier.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disableWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/disableWorkflow',
            workflow__pb2.WorkflowIdentifier.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enableWorkflow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/enableWorkflow',
            workflow__pb2.WorkflowIdentifier.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def listWorkflows(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ai_flow.WorkflowService/listWorkflows',
            workflow__pb2.ListWorkflowsRequest.SerializeToString,
            common__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
