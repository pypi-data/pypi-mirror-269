from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .protected_time_type import ProtectedTimeType
    from .schema_usage import SchemaUsage
    from .validation_error import ValidationError

from .protected_time_type import ProtectedTimeType

@dataclass
class RunSummary(ProtectedTimeType):
    # Array of datasets ids
    datasets: Optional[List[int]] = None
    # Run description
    description: Optional[str] = None
    # does Run have metadata uploaded alongside Run data
    has_metadata: Optional[bool] = None
    # Run unique ID
    id: Optional[int] = None
    # List of all Schema Usages for Run
    schemas: Optional[List[SchemaUsage]] = None
    # test ID run relates to
    testid: Optional[int] = None
    # test ID run relates to
    testname: Optional[str] = None
    # The token property
    token: Optional[str] = None
    # has Run been trashed in the UI
    trashed: Optional[bool] = None
    # Array of validation errors
    validation_errors: Optional[List[ValidationError]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> RunSummary:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunSummary
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return RunSummary()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .protected_time_type import ProtectedTimeType
        from .schema_usage import SchemaUsage
        from .validation_error import ValidationError

        from .protected_time_type import ProtectedTimeType
        from .schema_usage import SchemaUsage
        from .validation_error import ValidationError

        fields: Dict[str, Callable[[Any], None]] = {
            "datasets": lambda n : setattr(self, 'datasets', n.get_collection_of_primitive_values(int)),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "hasMetadata": lambda n : setattr(self, 'has_metadata', n.get_bool_value()),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "schemas": lambda n : setattr(self, 'schemas', n.get_collection_of_object_values(SchemaUsage)),
            "testid": lambda n : setattr(self, 'testid', n.get_int_value()),
            "testname": lambda n : setattr(self, 'testname', n.get_str_value()),
            "token": lambda n : setattr(self, 'token', n.get_str_value()),
            "trashed": lambda n : setattr(self, 'trashed', n.get_bool_value()),
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
        writer.write_collection_of_primitive_values("datasets", self.datasets)
        writer.write_str_value("description", self.description)
        writer.write_bool_value("hasMetadata", self.has_metadata)
        writer.write_int_value("id", self.id)
        writer.write_collection_of_object_values("schemas", self.schemas)
        writer.write_int_value("testid", self.testid)
        writer.write_str_value("testname", self.testname)
        writer.write_str_value("token", self.token)
        writer.write_bool_value("trashed", self.trashed)
        writer.write_collection_of_object_values("validationErrors", self.validation_errors)
    

