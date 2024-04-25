from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .indexed_label_value_map import IndexedLabelValueMap

from .indexed_label_value_map import IndexedLabelValueMap

@dataclass
class DatasetSummary_view(IndexedLabelValueMap):
    """
    map of view component ids to the LabelValueMap to render the component for this dataset
    """
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> DatasetSummary_view:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DatasetSummary_view
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return DatasetSummary_view()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .indexed_label_value_map import IndexedLabelValueMap

        from .indexed_label_value_map import IndexedLabelValueMap

        fields: Dict[str, Callable[[Any], None]] = {
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
    

