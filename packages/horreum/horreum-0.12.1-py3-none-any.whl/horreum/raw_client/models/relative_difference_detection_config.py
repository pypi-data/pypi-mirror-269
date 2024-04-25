from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class RelativeDifferenceDetectionConfig(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Built In
    built_in: Optional[bool] = None
    # Relative Difference Detection filter
    filter: Optional[str] = None
    # Minimal number of preceding datapoints
    min_previous: Optional[int] = None
    # Maximum difference between the aggregated value of last <window> datapoints and the mean of preceding values.
    threshold: Optional[float] = None
    # Number of most recent datapoints used for aggregating the value for comparison.
    window: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> RelativeDifferenceDetectionConfig:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RelativeDifferenceDetectionConfig
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return RelativeDifferenceDetectionConfig()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "builtIn": lambda n : setattr(self, 'built_in', n.get_bool_value()),
            "filter": lambda n : setattr(self, 'filter', n.get_str_value()),
            "minPrevious": lambda n : setattr(self, 'min_previous', n.get_int_value()),
            "threshold": lambda n : setattr(self, 'threshold', n.get_float_value()),
            "window": lambda n : setattr(self, 'window', n.get_int_value()),
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
        writer.write_bool_value("builtIn", self.built_in)
        writer.write_str_value("filter", self.filter)
        writer.write_int_value("minPrevious", self.min_previous)
        writer.write_float_value("threshold", self.threshold)
        writer.write_int_value("window", self.window)
        writer.write_additional_data_value(self.additional_data)
    

