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
    from .schema_post_response import SchemaPostResponse

class SchemaRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/run/{id}/schema
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new SchemaRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/run/{id}/schema{?path*}", path_parameters)
    
    async def post(self,body: Optional[str] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[SchemaPostResponse]:
        """
        Update Run schema for part of JSON data
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[SchemaPostResponse]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .schema_post_response import SchemaPostResponse

        return await self.request_adapter.send_async(request_info, SchemaPostResponse, None)
    
    def to_post_request_information(self,body: Optional[str] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Update Run schema for part of JSON data
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_scalar(self.request_adapter, "text/plain", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> SchemaRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: SchemaRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return SchemaRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class SchemaRequestBuilderPostQueryParameters():
        """
        Update Run schema for part of JSON data
        """
        # JSON path expression to update schema
        path: Optional[str] = None

    

