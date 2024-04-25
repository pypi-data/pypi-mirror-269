from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .fixed_threshold_detection_config_max import FixedThresholdDetectionConfig_max
    from .fixed_threshold_detection_config_min import FixedThresholdDetectionConfig_min

@dataclass
class FixedThresholdDetectionConfig(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Built In
    built_in: Optional[bool] = None
    # Upper bound for acceptable datapoint values
    max: Optional[FixedThresholdDetectionConfig_max] = None
    # Lower bound for acceptable datapoint values
    min: Optional[FixedThresholdDetectionConfig_min] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> FixedThresholdDetectionConfig:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: FixedThresholdDetectionConfig
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return FixedThresholdDetectionConfig()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .fixed_threshold_detection_config_max import FixedThresholdDetectionConfig_max
        from .fixed_threshold_detection_config_min import FixedThresholdDetectionConfig_min

        from .fixed_threshold_detection_config_max import FixedThresholdDetectionConfig_max
        from .fixed_threshold_detection_config_min import FixedThresholdDetectionConfig_min

        fields: Dict[str, Callable[[Any], None]] = {
            "builtIn": lambda n : setattr(self, 'built_in', n.get_bool_value()),
            "max": lambda n : setattr(self, 'max', n.get_object_value(FixedThresholdDetectionConfig_max)),
            "min": lambda n : setattr(self, 'min', n.get_object_value(FixedThresholdDetectionConfig_min)),
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
        writer.write_object_value("max", self.max)
        writer.write_object_value("min", self.min)
        writer.write_additional_data_value(self.additional_data)
    

