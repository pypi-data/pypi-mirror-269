from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_time_type import ProtectedTimeType
    from .validation_error import ValidationError

from .protected_time_type import ProtectedTimeType

@dataclass
class Dataset(ProtectedTimeType):
    """
    A dataset is the JSON document used as the basis for all comparisons and reporting
    """
    # Data payload
    data: Optional[str] = None
    # Run description
    description: Optional[str] = None
    # Dataset Unique ID
    id: Optional[int] = None
    # Dataset ordinal for ordered list of Datasets derived from a Run
    ordinal: Optional[int] = None
    # Run ID that Dataset relates to
    run_id: Optional[int] = None
    # Test ID that Dataset relates to
    testid: Optional[int] = None
    # List of Validation Errors
    validation_errors: Optional[List[ValidationError]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Dataset:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Dataset
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Dataset()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_time_type import ProtectedTimeType
        from .validation_error import ValidationError

        from .protected_time_type import ProtectedTimeType
        from .validation_error import ValidationError

        fields: Dict[str, Callable[[Any], None]] = {
            "data": lambda n : setattr(self, 'data', n.get_str_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "ordinal": lambda n : setattr(self, 'ordinal', n.get_int_value()),
            "runId": lambda n : setattr(self, 'run_id', n.get_int_value()),
            "testid": lambda n : setattr(self, 'testid', n.get_int_value()),
            "validationErrors": lambda n : setattr(self, 'validation_errors', n.get_collection_of_object_values(ValidationError)),
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
        writer.write_str_value("data", self.data)
        writer.write_str_value("description", self.description)
        writer.write_int_value("id", self.id)
        writer.write_int_value("ordinal", self.ordinal)
        writer.write_int_value("runId", self.run_id)
        writer.write_int_value("testid", self.testid)
        writer.write_collection_of_object_values("validationErrors", self.validation_errors)
    

