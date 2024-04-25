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
    from ....models.test_listing import TestListing

class SummaryRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/test/summary
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new SummaryRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/test/summary{?direction*,folder*,limit*,page*,roles*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[TestListing]:
        """
        Retrieve a summary of Tests in a folder
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[TestListing]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.test_listing import TestListing

        return await self.request_adapter.send_async(request_info, TestListing, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Retrieve a summary of Tests in a folder
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> SummaryRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: SummaryRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return SummaryRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class SummaryRequestBuilderGetQueryParameters():
        """
        Retrieve a summary of Tests in a folder
        """
        # Sort direction
        direction: Optional[str] = None

        # name of the Folder containing the Tests
        folder: Optional[str] = None

        # limit the result count
        limit: Optional[int] = None

        # filter by page number of a paginated list of 
        page: Optional[int] = None

        # "__my", "__all" or a comma delimited  list of roles
        roles: Optional[str] = None

    

