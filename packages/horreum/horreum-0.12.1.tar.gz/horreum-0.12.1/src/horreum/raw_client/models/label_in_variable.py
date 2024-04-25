from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .label_location import LabelLocation

from .label_location import LabelLocation

@dataclass
class LabelInVariable(LabelLocation):
    # The variableId property
    variable_id: Optional[int] = None
    # The variableName property
    variable_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> LabelInVariable:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: LabelInVariable
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return LabelInVariable()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .label_location import LabelLocation

        from .label_location import LabelLocation

        fields: Dict[str, Callable[[Any], None]] = {
            "variableId": lambda n : setattr(self, 'variable_id', n.get_int_value()),
            "variableName": lambda n : setattr(self, 'variable_name', n.get_str_value()),
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
        writer.write_int_value("variableId", self.variable_id)
        writer.write_str_value("variableName", self.variable_name)
    

