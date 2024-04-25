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
    from ....models.run import Run

class TestRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/run/test
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new TestRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/run/test{?access*,owner*,test*,token*}", path_parameters)
    
    async def post(self,body: Optional[Run] = None, request_configuration: Optional[RequestConfiguration] = None) -> bytes:
        """
        Upload a new Run
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: bytes
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "bytes", None)
    
    def to_post_request_information(self,body: Optional[Run] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
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
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> TestRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: TestRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return TestRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class TestRequestBuilderPostQueryParameters():
        """
        Upload a new Run
        """
        # New Access level
        access: Optional[Access] = None

        # Name of the new owner
        owner: Optional[str] = None

        # test name of ID
        test: Optional[str] = None

        # API token
        token: Optional[str] = None

    

