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
    from ....models.label_location import LabelLocation

class FindUsagesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/schema/findUsages
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new FindUsagesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/schema/findUsages?label={label}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[List[LabelLocation]]:
        """
        Find all usages of a Schema by label name
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[LabelLocation]]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.label_location import LabelLocation

        return await self.request_adapter.send_collection_async(request_info, LabelLocation, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Find all usages of a Schema by label name
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> FindUsagesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: FindUsagesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return FindUsagesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class FindUsagesRequestBuilderGetQueryParameters():
        """
        Find all usages of a Schema by label name
        """
        # Name of label to search for
        label: Optional[str] = None

    

