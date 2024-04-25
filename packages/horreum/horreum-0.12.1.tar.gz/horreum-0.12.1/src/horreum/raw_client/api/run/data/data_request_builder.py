from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ....models.access import Access

class DataRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/run/data
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new DataRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/run/data?start={start}&stop={stop}&test={test}{&access*,description*,owner*,schema*,token*}", path_parameters)
    
    async def post(self,body: Optional[str] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[int]:
        """
        Upload a new Run
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[int]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "int", None)
    
    def to_post_request_information(self,body: Optional[str] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Upload a new Run
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_scalar(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> DataRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DataRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return DataRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class DataRequestBuilderPostQueryParameters():
        """
        Upload a new Run
        """
        # New Access level
        access: Optional[Access] = None

        # Run description
        description: Optional[str] = None

        # Name of the new owner
        owner: Optional[str] = None

        # Schema URI
        schema: Optional[str] = None

        # start timestamp of run, or json path expression
        start: Optional[str] = None

        # stop timestamp of run, or json path expression
        stop: Optional[str] = None

        # test name of ID
        test: Optional[str] = None

        # Horreum internal token. Incompatible with Keycloak
        token: Optional[str] = None

    

