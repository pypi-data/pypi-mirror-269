# Copyright 2021-2023 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from ondewo.utils.base_services_interface import BaseServicesInterface

from ondewo.vtsi import calls_pb2
from ondewo.vtsi.calls_pb2_grpc import CallsStub


class Calls(BaseServicesInterface):
    """
    A class representing the Calls service interface.

    This class provides methods to interact with the Calls service, which allows starting and managing
    callers, listeners, scheduled callers, and handling calls and audio files.

    Inherits from BaseServicesInterface.
    """

    @property
    def stub(self) -> CallsStub:
        """
        Get the gRPC stub for the Calls service.

        Returns:
            CallsStub: The gRPC stub for the Calls service.
        """
        stub: CallsStub = CallsStub(channel=self.grpc_channel)
        return stub

    def start_caller(
        self,
        request: calls_pb2.StartCallerRequest,
    ) -> calls_pb2.StartCallerResponse:
        """
        Start a new caller.

        Args:
            request (calls_pb2.StartCallerRequest): The request message to start a new caller.

        Returns:
            calls_pb2.StartCallerResponse: The response message containing the caller ID and
            other details for the started caller.
        """
        return self.stub.StartCaller(request=request)

    def start_callers(
        self,
        request: calls_pb2.StartCallersRequest,
    ) -> calls_pb2.StartCallersResponse:
        """
        Start multiple callers.

        Args:
            request (calls_pb2.StartCallersRequest): The request message to start multiple callers.

        Returns:
            calls_pb2.StartCallersResponse: The response message containing the IDs and
            other details for the started callers.
        """
        return self.stub.StartCallers(request=request)

    def list_callers(
        self,
        request: calls_pb2.ListCallersRequest,
    ) -> calls_pb2.ListCallersResponse:
        """
        List all active callers.

        Args:
            request (calls_pb2.ListCallersRequest): The request message to list active callers.

        Returns:
            calls_pb2.ListCallersResponse: The response message containing a list of active callers.
        """
        return self.stub.ListCallers(request=request)

    def get_caller(
        self,
        request: calls_pb2.GetCallerRequest,
    ) -> calls_pb2.Caller:
        """
        Get details of a specific caller.

        Args:
            request (calls_pb2.GetCallerRequest): The request message to get details of a caller.

        Returns:
            calls_pb2.Caller: The response message containing the details of the specified caller.
        """
        return self.stub.GetCaller(request=request)

    def delete_caller(
        self,
        request: calls_pb2.DeleteCallersRequest,
    ) -> calls_pb2.DeleteCallersResponse:
        """
        Delete multiple callers.

        Args:
            request (calls_pb2.DeleteCallersRequest): The request message to delete multiple callers.

        Returns:
            calls_pb2.DeleteCallersResponse: The response message containing the IDs and
            other details for the deleted callers.
        """
        return self.stub.DeleteCallers(request=request)

    def delete_callers(
        self,
        request: calls_pb2.DeleteCallersRequest,
    ) -> calls_pb2.DeleteCallersResponse:
        """
        Delete multiple callers.

        Args:
            request (calls_pb2.DeleteCallersRequest): The request message to delete multiple callers.

        Returns:
            calls_pb2.DeleteCallersResponse: The response message containing the IDs and
            other details for the deleted callers.
        """
        return self.stub.DeleteCallers(request=request)

    def stop_caller(
        self,
        request: calls_pb2.StopCallersRequest,
    ) -> calls_pb2.StopCallersResponse:
        """
        Stop multiple callers.

        Args:
            request (calls_pb2.StopCallersRequest): The request message to stop multiple callers.

        Returns:
            calls_pb2.StopCallersResponse: The response message containing the IDs and
            other details for the stopd callers.
        """
        return self.stub.StopCallers(request=request)

    def stop_callers(
        self,
        request: calls_pb2.StopCallersRequest,
    ) -> calls_pb2.StopCallersResponse:
        """
        Stop multiple callers.

        Args:
            request (calls_pb2.StopCallersRequest): The request message to stop multiple callers.

        Returns:
            calls_pb2.StopCallersResponse: The response message containing the IDs and
            other details for the stopd callers.
        """
        return self.stub.StopCallers(request=request)

    def start_listener(
        self,
        request: calls_pb2.StartListenerRequest,
    ) -> calls_pb2.StartListenerResponse:
        """
        Start a new listener.

        Args:
            request (calls_pb2.StartListenerRequest): The request message to start a new listener.

        Returns:
            calls_pb2.StartListenerResponse: The response message containing the listener ID and
            other details for the started listener.
        """
        return self.stub.StartListener(request=request)

    def start_listeners(
        self,
        request: calls_pb2.StartListenersRequest,
    ) -> calls_pb2.StartListenersResponse:
        """
        Start multiple listeners.

        Args:
            request (calls_pb2.StartListenersRequest): The request message to start multiple listeners.

        Returns:
            calls_pb2.StartListenersResponse: The response message containing the IDs and
            other details for the started listeners.
        """
        return self.stub.StartListeners(request=request)

    def list_listeners(
        self,
        request: calls_pb2.ListListenersRequest,
    ) -> calls_pb2.ListListenersResponse:
        """
        List all active listeners.

        Args:
            request (calls_pb2.ListListenersRequest): The request message to list active listeners.

        Returns:
            calls_pb2.ListListenersResponse: The response message containing a list of active listeners.
        """
        return self.stub.ListListeners(request=request)

    def get_listener(
        self,
        request: calls_pb2.GetListenerRequest,
    ) -> calls_pb2.Listener:
        """
        Get details of a specific listener.

        Args:
            request (calls_pb2.GetListenerRequest): The request message to get details of a listener.

        Returns:
            calls_pb2.Listener: The response message containing the details of the specified listener.
        """
        return self.stub.GetListener(request=request)

    def delete_listener(
        self,
        request: calls_pb2.DeleteListenersRequest,
    ) -> calls_pb2.DeleteListenersResponse:
        """
        Delete multiple listeners.

        Args:
            request (calls_pb2.DeleteListenersRequest): The request message to delete multiple listeners.

        Returns:
            calls_pb2.DeleteListenersResponse: The response message containing the IDs and
            other details for the deleted listeners.
        """
        return self.stub.DeleteListeners(request=request)

    def delete_listeners(
        self,
        request: calls_pb2.DeleteListenersRequest,
    ) -> calls_pb2.DeleteListenersResponse:
        """
        Delete multiple listeners.

        Args:
            request (calls_pb2.DeleteListenersRequest): The request message to delete multiple listeners.

        Returns:
            calls_pb2.DeleteListenersResponse: The response message containing the IDs and
            other details for the deleted listeners.
        """
        return self.stub.DeleteListeners(request=request)

    def stop_listener(
        self,
        request: calls_pb2.StopListenersRequest,
    ) -> calls_pb2.StopListenersResponse:
        """
        Stop multiple listeners.

        Args:
            request (calls_pb2.StopListenersRequest): The request message to stop multiple listeners.

        Returns:
            calls_pb2.StopListenersResponse: The response message containing the IDs and
            other details for the stopd listeners.
        """
        return self.stub.StopListeners(request=request)

    def stop_listeners(
        self,
        request: calls_pb2.StopListenersRequest,
    ) -> calls_pb2.StopListenersResponse:
        """
        Stop multiple listeners.

        Args:
            request (calls_pb2.StopListenersRequest): The request message to stop multiple listeners.

        Returns:
            calls_pb2.StopListenersResponse: The response message containing the IDs and
            other details for the stopd listeners.
        """
        return self.stub.StopListeners(request=request)

    def start_scheduled_caller(
        self,
        request: calls_pb2.StartScheduledCallerRequest
    ) -> calls_pb2.StartScheduledCallerResponse:
        """
        Start a new scheduled caller.

        Args:
            request (calls_pb2.StartScheduledCallerRequest): The request message to start a new scheduled caller.

        Returns:
            calls_pb2.StartScheduledCallerResponse: The response message containing the scheduled caller ID and
            other details for the started scheduled caller.
        """
        return self.stub.StartScheduledCaller(request=request)

    def start_scheduled_callers(
        self,
        request: calls_pb2.StartScheduledCallersRequest,
    ) -> calls_pb2.StartScheduledCallersResponse:
        """
        Start multiple scheduled callers.

        Args:
            request (calls_pb2.StartScheduledCallersRequest): The request message to start multiple scheduled callers.

        Returns:
            calls_pb2.StartScheduledCallersResponse: The response message containing the IDs and
            other details for the started scheduled callers.
        """
        return self.stub.StartScheduledCallers(request=request)

    def stop_call(
        self,
        request: calls_pb2.StopCallRequest,
    ) -> calls_pb2.StopCallResponse:
        """
        Stop an active call.

        Args:
            request (calls_pb2.StopCallRequest): The request message to stop an active call.

        Returns:
            calls_pb2.StopCallResponse: The response message containing the details of the stopped call.
        """
        return self.stub.StopCall(request=request)

    def stop_calls(
        self, request:
        calls_pb2.StopCallsRequest,
    ) -> calls_pb2.StopCallsResponse:
        """
        Stop multiple active calls.

        Args:
            request (calls_pb2.StopCallsRequest): The request message to stop multiple active calls.

        Returns:
            calls_pb2.StopCallsResponse: The response message containing the details of the stopped calls.
        """
        return self.stub.StopCalls(request=request)

    def stop_all_calls(
        self,
        request: calls_pb2.StopAllCallsRequest,
    ) -> calls_pb2.StopCallsResponse:
        """
        Stop all active calls.

        Args:
            request (calls_pb2.StopAllCallsRequest): The request message to stop all active calls.

        Returns:
            calls_pb2.StopCallsResponse: The response message containing the details of the stopped calls.
        """
        return self.stub.StopAllCalls(request=request)

    def transfer_call(
        self,
        request: calls_pb2.TransferCallRequest,
    ) -> calls_pb2.TransferCallResponse:
        """
        Transfer an active call to a different entity.

        Args:
            request (calls_pb2.TransferCallRequest): The request message to transfer an active call.

        Returns:
            calls_pb2.TransferCallResponse: The response message containing the details of the transferred call.
        """
        return self.stub.TransferCall(request=request)

    def transfer_calls(
        self,
        request: calls_pb2.TransferCallsRequest,
    ) -> calls_pb2.TransferCallsResponse:
        """
        Transfer multiple active calls to different entities.

        Args:
            request (calls_pb2.TransferCallsRequest): The request message to transfer multiple active calls.

        Returns:
            calls_pb2.TransferCallsResponse: The response message containing the details of the transferred calls.
        """
        return self.stub.TransferCalls(request=request)

    def get_call(
        self,
        request: calls_pb2.GetCallRequest
    ) -> calls_pb2.Call:
        """
        Get details of a specific call.

        Args:
            request (calls_pb2.GetCallRequest): The request message to get details of a call.

        Returns:
            calls_pb2.Call: The response message containing the details of the specified call.
        """
        return self.stub.GetCall(request=request)

    def list_calls(
        self,
        request: calls_pb2.ListCallsRequest,
    ) -> calls_pb2.ListCallsResponse:
        """
        List all active calls.

        Args:
            request (calls_pb2.ListCallsRequest): The request message to list active calls.

        Returns:
            calls_pb2.ListCallsResponse: The response message containing a list of active calls.
        """
        return self.stub.ListCalls(request=request)
