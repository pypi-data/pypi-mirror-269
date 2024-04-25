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
    from .....models.experiment_profile import ExperimentProfile
    from .item.with_profile_item_request_builder import WithProfileItemRequestBuilder

class ProfilesRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /api/experiment/{testId}/profiles
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new ProfilesRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/api/experiment/{testId}/profiles", path_parameters)
    
    def by_profile_id(self,profile_id: int) -> WithProfileItemRequestBuilder:
        """
        Gets an item from the raw_client.api.experiment.item.profiles.item collection
        param profile_id: Experiment Profile ID
        Returns: WithProfileItemRequestBuilder
        """
        if not profile_id:
            raise TypeError("profile_id cannot be null.")
        from .item.with_profile_item_request_builder import WithProfileItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["profileId"] = profile_id
        return WithProfileItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration] = None) -> Optional[List[ExperimentProfile]]:
        """
        Retrieve Experiment Profiles by Test ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[List[ExperimentProfile]]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from .....models.experiment_profile import ExperimentProfile

        return await self.request_adapter.send_collection_async(request_info, ExperimentProfile, None)
    
    async def post(self,body: Optional[ExperimentProfile] = None, request_configuration: Optional[RequestConfiguration] = None) -> Optional[int]:
        """
        Save new or update existing Experiment Profiles for a Test 
        param body: An Experiment Profile defines the labels and filters for the dataset and baseline
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[int]
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        return await self.request_adapter.send_primitive_async(request_info, "int", None)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Retrieve Experiment Profiles by Test ID
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: Optional[ExperimentProfile] = None, request_configuration: Optional[RequestConfiguration] = None) -> RequestInformation:
        """
        Save new or update existing Experiment Profiles for a Test 
        param body: An Experiment Profile defines the labels and filters for the dataset and baseline
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if not body:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "application/json", body)
        return request_info
    
    def with_url(self,raw_url: Optional[str] = None) -> ProfilesRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: ProfilesRequestBuilder
        """
        if not raw_url:
            raise TypeError("raw_url cannot be null.")
        return ProfilesRequestBuilder(self.request_adapter, raw_url)
    

