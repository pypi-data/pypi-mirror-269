from __future__ import annotations
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_token_item_request_builder import WithTokenItemRequestBuilder

class RevokeTokenRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/test/{id}/revokeToken
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new RevokeTokenRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/test/{id}/revokeToken", path_parameters)
    
    def by_token_id(self,token_id: int) -> WithTokenItemRequestBuilder:
        """
        Gets an item from the raw_client.api.test.item.revokeToken.item collection
        param token_id: ID of token to revoke
        Returns: WithTokenItemRequestBuilder
        """
        if not token_id:
            raise TypeError("token_id cannot be null.")
        from .item.with_token_item_request_builder import WithTokenItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["tokenId"] = token_id
        return WithTokenItemRequestBuilder(self.request_adapter, url_tpl_params)
    

