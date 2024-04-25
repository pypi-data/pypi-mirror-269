from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .dataset_summary_view import DatasetSummary_view
    from .protected_time_type import ProtectedTimeType
    from .schema_usage import SchemaUsage
    from .validation_error import ValidationError

from .protected_time_type import ProtectedTimeType

@dataclass
class DatasetSummary(ProtectedTimeType):
    # Dataset description
    description: Optional[str] = None
    # Unique Dataset ID
    id: Optional[int] = None
    # Ordinal position of Dataset Summary on returned List
    ordinal: Optional[int] = None
    # Run ID that Dataset relates to
    run_id: Optional[int] = None
    # List of Schema usages
    schemas: Optional[List[SchemaUsage]] = None
    # Test ID that Dataset relates to
    test_id: Optional[int] = None
    # Test name that the Dataset relates to
    testname: Optional[str] = None
    # List of Validation Errors
    validation_errors: Optional[List[ValidationError]] = None
    # map of view component ids to the LabelValueMap to render the component for this dataset
    view: Optional[DatasetSummary_view] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> DatasetSummary:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DatasetSummary
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return DatasetSummary()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .dataset_summary_view import DatasetSummary_view
        from .protected_time_type import ProtectedTimeType
        from .schema_usage import SchemaUsage
        from .validation_error import ValidationError

        from .dataset_summary_view import DatasetSummary_view
        from .protected_time_type import ProtectedTimeType
        from .schema_usage import SchemaUsage
        from .validation_error import ValidationError

        fields: Dict[str, Callable[[Any], None]] = {
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "ordinal": lambda n : setattr(self, 'ordinal', n.get_int_value()),
            "runId": lambda n : setattr(self, 'run_id', n.get_int_value()),
            "schemas": lambda n : setattr(self, 'schemas', n.get_collection_of_object_values(SchemaUsage)),
            "testId": lambda n : setattr(self, 'test_id', n.get_int_value()),
            "testname": lambda n : setattr(self, 'testname', n.get_str_value()),
            "validationErrors": lambda n : setattr(self, 'validation_errors', n.get_collection_of_object_values(ValidationError)),
            "view": lambda n : setattr(self, 'view', n.get_object_value(DatasetSummary_view)),
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
        writer.write_str_value("description", self.description)
        writer.write_int_value("id", self.id)
        writer.write_int_value("ordinal", self.ordinal)
        writer.write_int_value("runId", self.run_id)
        writer.write_collection_of_object_values("schemas", self.schemas)
        writer.write_int_value("testId", self.test_id)
        writer.write_str_value("testname", self.testname)
        writer.write_collection_of_object_values("validationErrors", self.validation_errors)
        writer.write_object_value("view", self.view)
    

