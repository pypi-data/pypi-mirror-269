from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .extractor import Extractor
    from .protected_type import ProtectedType

from .protected_type import ProtectedType

@dataclass
class Transformer(ProtectedType):
    """
    A transformer extracts labals and applies a Function to convert a Run into one or more Datasets
    """
    # Transformer description
    description: Optional[str] = None
    # A collection of extractors to extract JSON values to create new Dataset JSON document
    extractors: Optional[List[Extractor]] = None
    # The function property
    function: Optional[str] = None
    # Unique Transformer id
    id: Optional[int] = None
    # Transformer name
    name: Optional[str] = None
    # Schema ID that the transform is registered against
    schema_id: Optional[int] = None
    # Schema name that the transform is registered against
    schema_name: Optional[str] = None
    # Schema Uri that the transform is registered against
    schema_uri: Optional[str] = None
    # The schema associated with the calculated Datasets. Where a transformer creates a new JSON object with a new structure, this Schema is used to extafct values from the new Dataset JSON document
    target_schema_uri: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Transformer:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Transformer
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Transformer()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .extractor import Extractor
        from .protected_type import ProtectedType

        from .extractor import Extractor
        from .protected_type import ProtectedType

        fields: Dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "extractors": lambda n : setattr(self, 'extractors', n.get_collection_of_object_values(Extractor)),
            "function": lambda n : setattr(self, 'function', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "schemaId": lambda n : setattr(self, 'schema_id', n.get_int_value()),
            "schemaName": lambda n : setattr(self, 'schema_name', n.get_str_value()),
            "schemaUri": lambda n : setattr(self, 'schema_uri', n.get_str_value()),
            "targetSchemaUri": lambda n : setattr(self, 'target_schema_uri', n.get_str_value()),
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
        writer.write_str_value("description", self.description)
        writer.write_collection_of_object_values("extractors", self.extractors)
        writer.write_str_value("function", self.function)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_int_value("schemaId", self.schema_id)
        writer.write_str_value("schemaName", self.schema_name)
        writer.write_str_value("schemaUri", self.schema_uri)
        writer.write_str_value("targetSchemaUri", self.target_schema_uri)
    

