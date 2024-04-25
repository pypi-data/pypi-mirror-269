from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .label_value_schema import LabelValue_schema

@dataclass
class LabelValue(AdditionalDataHolder, Parsable):
    """
    Label Value derived from Label definition and Dataset Data
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Unique ID for Label Value
    id: Optional[int] = None
    # Label name
    name: Optional[str] = None
    # Summary description of Schema
    schema: Optional[LabelValue_schema] = None
    # Value value extracted from Dataset. This can be a scalar, array or JSON object
    value: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> LabelValue:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: LabelValue
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return LabelValue()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .label_value_schema import LabelValue_schema

        from .label_value_schema import LabelValue_schema

        fields: Dict[str, Callable[[Any], None]] = {
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "schema": lambda n : setattr(self, 'schema', n.get_object_value(LabelValue_schema)),
            "value": lambda n : setattr(self, 'value', n.get_str_value()),
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
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_object_value("schema", self.schema)
        writer.write_str_value("value", self.value)
        writer.write_additional_data_value(self.additional_data)
    

