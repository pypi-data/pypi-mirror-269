from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .label import Label
    from .schema import Schema
    from .transformer import Transformer

from .schema import Schema

@dataclass
class SchemaExport(Schema):
    """
    Represents a Schema with all associated data used for export/import operations.
    """
    # Array of Labels associated with schema
    labels: Optional[List[Label]] = None
    # Array of Transformers associated with schema
    transformers: Optional[List[Transformer]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> SchemaExport:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SchemaExport
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return SchemaExport()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .label import Label
        from .schema import Schema
        from .transformer import Transformer

        from .label import Label
        from .schema import Schema
        from .transformer import Transformer

        fields: Dict[str, Callable[[Any], None]] = {
            "labels": lambda n : setattr(self, 'labels', n.get_collection_of_object_values(Label)),
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
        writer.write_collection_of_object_values("labels", self.labels)
        writer.write_collection_of_object_values("transformers", self.transformers)
    

