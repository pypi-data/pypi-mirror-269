from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .change_detection_config import ChangeDetection_config
    from .fixed_threshold_detection_config import FixedThresholdDetectionConfig
    from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

@dataclass
class ChangeDetection(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The config property
    config: Optional[ChangeDetection_config] = None
    # The id property
    id: Optional[int] = None
    # The model property
    model: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> ChangeDetection:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChangeDetection
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return ChangeDetection()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .change_detection_config import ChangeDetection_config
        from .fixed_threshold_detection_config import FixedThresholdDetectionConfig
        from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

        from .change_detection_config import ChangeDetection_config
        from .fixed_threshold_detection_config import FixedThresholdDetectionConfig
        from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

        fields: Dict[str, Callable[[Any], None]] = {
            "config": lambda n : setattr(self, 'config', n.get_object_value(ChangeDetection_config)),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "model": lambda n : setattr(self, 'model', n.get_str_value()),
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
        writer.write_object_value("config", self.config)
        writer.write_int_value("id", self.id)
        writer.write_str_value("model", self.model)
        writer.write_additional_data_value(self.additional_data)
    
    from kiota_abstractions.serialization import ComposedTypeWrapper

    @dataclass
    class ChangeDetection_config(ComposedTypeWrapper, Parsable):
        from kiota_abstractions.serialization import ComposedTypeWrapper

        if TYPE_CHECKING:
            from .fixed_threshold_detection_config import FixedThresholdDetectionConfig
            from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

        """
        Composed type wrapper for classes FixedThresholdDetectionConfig, RelativeDifferenceDetectionConfig
        """
        @staticmethod
        def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> ChangeDetection_config:
            """
            Creates a new instance of the appropriate class based on discriminator value
            param parse_node: The parse node to use to read the discriminator value and create the object
            Returns: ChangeDetection_config
            """
            if not parse_node:
                raise TypeError("parse_node cannot be null.")
            try:
                mapping_value = parse_node.get_child_node("model").get_str_value()
            except AttributeError:
                mapping_value = None
            result = ChangeDetection_config()
            if mapping_value and mapping_value.casefold() == "fixedThreshold".casefold():
                from .fixed_threshold_detection_config import FixedThresholdDetectionConfig

                result.fixed_threshold_detection_config = FixedThresholdDetectionConfig()
            elif mapping_value and mapping_value.casefold() == "relativeDifference".casefold():
                from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

                result.relative_difference_detection_config = RelativeDifferenceDetectionConfig()
            return result
        
        def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
            """
            The deserialization information for the current model
            Returns: Dict[str, Callable[[ParseNode], None]]
            """
            from .fixed_threshold_detection_config import FixedThresholdDetectionConfig
            from .relative_difference_detection_config import RelativeDifferenceDetectionConfig

            if self.fixed_threshold_detection_config:
                return self.fixed_threshold_detection_config.get_field_deserializers()
            if self.relative_difference_detection_config:
                return self.relative_difference_detection_config.get_field_deserializers()
            return {}
        
        def serialize(self,writer: SerializationWriter) -> None:
            """
            Serializes information the current object
            param writer: Serialization writer to use to serialize this model
            Returns: None
            """
            if not writer:
                raise TypeError("writer cannot be null.")
            if self.fixed_threshold_detection_config:
                writer.write_object_value(None, self.fixed_threshold_detection_config)
            elif self.relative_difference_detection_config:
                writer.write_object_value(None, self.relative_difference_detection_config)
        
    

