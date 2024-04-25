from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_type import ProtectedType
    from .test_token import TestToken
    from .transformer import Transformer

from .protected_type import ProtectedType

@dataclass
class Test(ProtectedType):
    """
    Represents a Test. Tests are typically equivalent to a particular benchmark
    """
    # URL to external service that can be called to compare runs.  This is typically an external reporting/visulization service
    compare_url: Optional[str] = None
    # backend ID for backing datastore
    datastore_id: Optional[int] = None
    # Description of the test
    description: Optional[str] = None
    # Filter function to filter out datasets that are comparable for the purpose of change detection
    fingerprint_filter: Optional[str] = None
    # Array of Label names that are used to create a fingerprint 
    fingerprint_labels: Optional[List[str]] = None
    # Name of folder that the test is stored in. Folders allow tests to be organised in the UI
    folder: Optional[str] = None
    # Unique Test id
    id: Optional[int] = None
    # Test name
    name: Optional[str] = None
    # Are notifications enabled for the test
    notifications_enabled: Optional[bool] = None
    # Label function to modify timeline labels to a produce a value used for ordering datapoints
    timeline_function: Optional[str] = None
    # List of label names that are used for determining metric to use as the time series
    timeline_labels: Optional[List[str]] = None
    # Array of API tokens associated with test
    tokens: Optional[List[TestToken]] = None
    # Array for transformers defined for the Test
    transformers: Optional[List[Transformer]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Test:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Test
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Test()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_type import ProtectedType
        from .test_token import TestToken
        from .transformer import Transformer

        from .protected_type import ProtectedType
        from .test_token import TestToken
        from .transformer import Transformer

        fields: Dict[str, Callable[[Any], None]] = {
            "compareUrl": lambda n : setattr(self, 'compare_url', n.get_str_value()),
            "datastoreId": lambda n : setattr(self, 'datastore_id', n.get_int_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "fingerprintFilter": lambda n : setattr(self, 'fingerprint_filter', n.get_str_value()),
            "fingerprintLabels": lambda n : setattr(self, 'fingerprint_labels', n.get_collection_of_primitive_values(str)),
            "folder": lambda n : setattr(self, 'folder', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "notificationsEnabled": lambda n : setattr(self, 'notifications_enabled', n.get_bool_value()),
            "timelineFunction": lambda n : setattr(self, 'timeline_function', n.get_str_value()),
            "timelineLabels": lambda n : setattr(self, 'timeline_labels', n.get_collection_of_primitive_values(str)),
            "tokens": lambda n : setattr(self, 'tokens', n.get_collection_of_object_values(TestToken)),
            "transformers": lambda n : setattr(self, 'transformers', n.get_collection_of_object_values(Transformer)),
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
        writer.write_str_value("compareUrl", self.compare_url)
        writer.write_int_value("datastoreId", self.datastore_id)
        writer.write_str_value("description", self.description)
        writer.write_str_value("fingerprintFilter", self.fingerprint_filter)
        writer.write_collection_of_primitive_values("fingerprintLabels", self.fingerprint_labels)
        writer.write_str_value("folder", self.folder)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("notificationsEnabled", self.notifications_enabled)
        writer.write_str_value("timelineFunction", self.timeline_function)
        writer.write_collection_of_primitive_values("timelineLabels", self.timeline_labels)
        writer.write_collection_of_object_values("tokens", self.tokens)
        writer.write_collection_of_object_values("transformers", self.transformers)
    

