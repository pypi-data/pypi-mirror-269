from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_type import ProtectedType

from .protected_type import ProtectedType

@dataclass
class Schema(ProtectedType):
    """
    Data object that describes the schema definition for a test
    """
    # Schema Description
    description: Optional[str] = None
    # Unique Schema ID
    id: Optional[int] = None
    # Schema name
    name: Optional[str] = None
    # JSON validation schema. Used to validate uploaded JSON documents
    schema: Optional[str] = None
    # Array of API tokens associated with test
    token: Optional[str] = None
    # Unique, versioned schema URI
    uri: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Schema:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Schema
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Schema()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_type import ProtectedType

        from .protected_type import ProtectedType

        fields: Dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "schema": lambda n : setattr(self, 'schema', n.get_str_value()),
            "token": lambda n : setattr(self, 'token', n.get_str_value()),
            "uri": lambda n : setattr(self, 'uri', n.get_str_value()),
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
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_str_value("schema", self.schema)
        writer.write_str_value("token", self.token)
        writer.write_str_value("uri", self.uri)
    

