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
    from .metadata_get_response import MetadataGetResponse

class MetadataRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/run/{id}/metadata
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new MetadataRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/run/{id}/metadata{?schemaUri*,token*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[MetadataGetResponse]:
        """
        Get Run  meta data by Run ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[MetadataGetResponse]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .metadata_get_response import MetadataGetResponse

        return await self.request_adapter.send_async(request_info, MetadataGetResponse, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Get Run  meta data by Run ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> MetadataRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: MetadataRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return MetadataRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class MetadataRequestBuilderGetQueryParameters():
        """
        Get Run  meta data by Run ID
        """
        def get_query_parameter(self,original_name: Optional[str] = None) -> str:
            """
            Maps the query parameters names to their encoded names for the URI template parsing.
            param original_name: The original query parameter name in the class.
            Returns: str
            """
            if not original_name:
                raise TypeError("original_name cannot be null.")
            if original_name == "schema_uri":
                return "schemaUri"
            if original_name == "token":
                return "token"
            return original_name
        
        # Filter by Schmea URI
        schema_uri: Optional[str] = None

        # Run API token
        token: Optional[str] = None

    

