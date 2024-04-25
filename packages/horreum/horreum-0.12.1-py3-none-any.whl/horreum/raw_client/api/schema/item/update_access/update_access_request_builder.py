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
    from .....models.access import Access

class UpdateAccessRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/schema/{id-id}/updateAccess
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new UpdateAccessRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/schema/{id%2Did}/updateAccess?access={access}&owner={owner}", path_parameters)
    
    async def post(self,request_configuration: Optional[RequestConfiguration] = None) -> None:
        """
        Update the Access configuration for a Schema
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: None
        """
        request_info = self.to_post_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_no_response_content_async(request_info, None)
    
    def to_post_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Update the Access configuration for a Schema
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> UpdateAccessRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: UpdateAccessRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return UpdateAccessRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class UpdateAccessRequestBuilderPostQueryParameters():
        """
        Update the Access configuration for a Schema
        """
        # New Access level
        access: Optional[Access] = None

        # Name of the new owner
        owner: Optional[str] = None

    

