from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .label_location import LabelLocation

from .label_location import LabelLocation

@dataclass
class LabelInReport(LabelLocation):
    # The configId property
    config_id: Optional[int] = None
    # The name property
    name: Optional[str] = None
    # The title property
    title: Optional[str] = None
    # The where property
    where: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> LabelInReport:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: LabelInReport
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return LabelInReport()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .label_location import LabelLocation

        from .label_location import LabelLocation

        fields: Dict[str, Callable[[Any], None]] = {
            "configId": lambda n : setattr(self, 'config_id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "title": lambda n : setattr(self, 'title', n.get_str_value()),
            "where": lambda n : setattr(self, 'where', n.get_str_value()),
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
        writer.write_int_value("configId", self.config_id)
        writer.write_str_value("name", self.name)
        writer.write_str_value("title", self.title)
        writer.write_str_value("where", self.where)
    

