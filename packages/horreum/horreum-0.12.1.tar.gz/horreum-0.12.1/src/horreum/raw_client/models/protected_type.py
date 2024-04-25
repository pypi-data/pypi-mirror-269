from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_type_access import ProtectedType_access

@dataclass
class ProtectedType(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Access rights for the test. This defines the visibility of the Test in the UI
    access: Optional[ProtectedType_access] = None
    # Name of the team that owns the test. Users must belong to the team that owns a test to make modifications
    owner: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> ProtectedType:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ProtectedType
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ProtectedType()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_type_access import ProtectedType_access

        from .protected_type_access import ProtectedType_access

        fields: Dict[str, Callable[[Any], None]] = {
            "access": lambda n : setattr(self, 'access', n.get_enum_value(ProtectedType_access)),
            "owner": lambda n : setattr(self, 'owner', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if not writer:
            raise TypeError("writer cannot be null.")
        writer.write_enum_value("access", self.access)
        writer.write_str_value("owner", self.owner)
        writer.write_additional_data_value(self.additional_data)
    

