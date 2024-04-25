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
    from .....models.exported_label_values import ExportedLabelValues

class LabelValuesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/test/{id}/labelValues
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new LabelValuesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/test/{id}/labelValues{?after*,before*,direction*,filter*,filtering*,limit*,metrics*,page*,sort*}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[List[ExportedLabelValues]]:
        """
        List all Label Values for a Test
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[ExportedLabelValues]]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.exported_label_values import ExportedLabelValues

        return await self.request_adapter.send_collection_async(request_info, ExportedLabelValues, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        List all Label Values for a Test
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> LabelValuesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: LabelValuesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return LabelValuesRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class LabelValuesRequestBuilderGetQueryParameters():
        """
        List all Label Values for a Test
        """
        # ISO-like date time string or epoch millis
        after: Optional[str] = None

        # ISO-like date time string or epoch millis
        before: Optional[str] = None

        # either Ascending or Descending
        direction: Optional[str] = None

        # either a required json sub-document or path expression
        filter: Optional[str] = None

        # Retrieve values for Filtering Labels
        filtering: Optional[bool] = None

        # the maximum number of results to include
        limit: Optional[int] = None

        # Retrieve values for Metric Labels
        metrics: Optional[bool] = None

        # which page to skip to when using a limit
        page: Optional[int] = None

        # json path to sortable value or start or stop for sorting by time
        sort: Optional[str] = None

    

