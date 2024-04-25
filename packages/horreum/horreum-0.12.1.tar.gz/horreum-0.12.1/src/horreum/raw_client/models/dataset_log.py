from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .persistent_log import PersistentLog

from .persistent_log import PersistentLog

@dataclass
class DatasetLog(PersistentLog):
    """
    Dataset Log
    """
    # The datasetId property
    dataset_id: Optional[int] = None
    # The datasetOrdinal property
    dataset_ordinal: Optional[int] = None
    # The runId property
    run_id: Optional[int] = None
    # The source property
    source: Optional[str] = None
    # The testId property
    test_id: Optional[int] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> DatasetLog:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DatasetLog
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return DatasetLog()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .persistent_log import PersistentLog

        from .persistent_log import PersistentLog

        fields: Dict[str, Callable[[Any], None]] = {
            "datasetId": lambda n : setattr(self, 'dataset_id', n.get_int_value()),
            "datasetOrdinal": lambda n : setattr(self, 'dataset_ordinal', n.get_int_value()),
            "runId": lambda n : setattr(self, 'run_id', n.get_int_value()),
            "source": lambda n : setattr(self, 'source', n.get_str_value()),
            "testId": lambda n : setattr(self, 'test_id', n.get_int_value()),
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
        writer.write_int_value("datasetId", self.dataset_id)
        writer.write_int_value("datasetOrdinal", self.dataset_ordinal)
        writer.write_int_value("runId", self.run_id)
        writer.write_str_value("source", self.source)
        writer.write_int_value("testId", self.test_id)
    

