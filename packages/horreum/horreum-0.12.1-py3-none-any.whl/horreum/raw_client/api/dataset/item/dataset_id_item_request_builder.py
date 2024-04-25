from __future__ import annotations
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
    from ....models.dataset import Dataset
    from .label_values.label_values_request_builder import LabelValuesRequestBuilder
    from .preview_label.preview_label_request_builder import PreviewLabelRequestBuilder
    from .summary.summary_request_builder import SummaryRequestBuilder

class DatasetIdItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/dataset/{datasetId-id}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new DatasetIdItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/dataset/{datasetId%2Did}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[Dataset]:
        """
        Retrieve Dataset by ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Dataset]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.dataset import Dataset

        return await self.request_adapter.send_async(request_info, Dataset, None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Retrieve Dataset by ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> DatasetIdItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: DatasetIdItemRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return DatasetIdItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def label_values(self) -> LabelValuesRequestBuilder:
        """
        The labelValues property
        """
        from .label_values.label_values_request_builder import LabelValuesRequestBuilder

        return LabelValuesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def preview_label(self) -> PreviewLabelRequestBuilder:
        """
        The previewLabel property
        """
        from .preview_label.preview_label_request_builder import PreviewLabelRequestBuilder

        return PreviewLabelRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def summary(self) -> SummaryRequestBuilder:
        """
        The summary property
        """
        from .summary.summary_request_builder import SummaryRequestBuilder

        return SummaryRequestBuilder(self.request_adapter, self.path_parameters)
    

