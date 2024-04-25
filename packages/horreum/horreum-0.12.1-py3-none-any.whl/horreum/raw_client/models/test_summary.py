from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_type import ProtectedType

from .protected_type import ProtectedType

@dataclass
class TestSummary(ProtectedType):
    # Total number of Datasets for the Test
    datasets: Optional[float] = None
    # Datastore id
    datastore_id: Optional[int] = None
    # Description of the test
    description: Optional[str] = None
    # Name of folder that the test is stored in. Folders allow tests to be organised in the UI
    folder: Optional[str] = None
    # ID of tests
    id: Optional[int] = None
    # Test name
    name: Optional[str] = None
    # Total number of Runs for the Test
    runs: Optional[float] = None
    # Subscriptions for each test for authenticated user
    watching: Optional[List[str]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> TestSummary:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TestSummary
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return TestSummary()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_type import ProtectedType

        from .protected_type import ProtectedType

        fields: Dict[str, Callable[[Any], None]] = {
            "datasets": lambda n : setattr(self, 'datasets', n.get_float_value()),
            "datastoreId": lambda n : setattr(self, 'datastore_id', n.get_int_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "folder": lambda n : setattr(self, 'folder', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "runs": lambda n : setattr(self, 'runs', n.get_float_value()),
            "watching": lambda n : setattr(self, 'watching', n.get_collection_of_primitive_values(str)),
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
        writer.write_float_value("datasets", self.datasets)
        writer.write_int_value("datastoreId", self.datastore_id)
        writer.write_str_value("description", self.description)
        writer.write_str_value("folder", self.folder)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_float_value("runs", self.runs)
        writer.write_collection_of_primitive_values("watching", self.watching)
    

