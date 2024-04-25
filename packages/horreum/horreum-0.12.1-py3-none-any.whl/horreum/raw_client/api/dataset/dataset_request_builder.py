from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .by_schema.by_schema_request_builder import BySchemaRequestBuilder
    from .item.dataset_id_item_request_builder import DatasetIdItemRequestBuilder
    from .list_.list_request_builder import ListRequestBuilder

class DatasetRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/dataset
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new DatasetRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/dataset", path_parameters)
    
    def by_dataset_id_id(self,dataset_id_id: int) -> DatasetIdItemRequestBuilder:
        """
        Gets an item from the raw_client.api.dataset.item collection
        param dataset_id_id: Dataset ID to retrieve
        Returns: DatasetIdItemRequestBuilder
        """
        if not dataset_id_id:
            raise TypeError("dataset_id_id cannot be null.")
        from .item.dataset_id_item_request_builder import DatasetIdItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["datasetId%2Did"] = dataset_id_id
        return DatasetIdItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    @property
    def by_schema(self) -> BySchemaRequestBuilder:
        """
        The bySchema property
        """
        from .by_schema.by_schema_request_builder import BySchemaRequestBuilder

        return BySchemaRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def list_(self) -> ListRequestBuilder:
        """
        The list property
        """
        from .list_.list_request_builder import ListRequestBuilder

        return ListRequestBuilder(self.request_adapter, self.path_parameters)
    

