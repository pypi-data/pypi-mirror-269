from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .datastore_access import Datastore_access
    from .datastore_config import Datastore_config
    from .datastore_type import Datastore_type
    from .elasticsearch_datastore_config import ElasticsearchDatastoreConfig
    from .postgres_datastore_config import PostgresDatastoreConfig

@dataclass
class Datastore(AdditionalDataHolder, Parsable):
    """
    Type of backend datastore
    """
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # Access rights for the test. This defines the visibility of the Test in the UI
    access: Optional[Datastore_access] = None
    # Is this a built-in datastore? Built-in datastores cannot be deleted or modified
    built_in: Optional[bool] = None
    # The config property
    config: Optional[Datastore_config] = None
    # Unique Datastore id
    id: Optional[int] = None
    # Name of the datastore, used to identify the datastore in the Test definition
    name: Optional[str] = None
    # Name of the team that owns the test. Users must belong to the team that owns a test to make modifications
    owner: Optional[str] = None
    # Type of backend datastore
    type: Optional[Datastore_type] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Datastore:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Datastore
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return Datastore()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .datastore_access import Datastore_access
        from .datastore_config import Datastore_config
        from .datastore_type import Datastore_type
        from .elasticsearch_datastore_config import ElasticsearchDatastoreConfig
        from .postgres_datastore_config import PostgresDatastoreConfig

        from .datastore_access import Datastore_access
        from .datastore_config import Datastore_config
        from .datastore_type import Datastore_type
        from .elasticsearch_datastore_config import ElasticsearchDatastoreConfig
        from .postgres_datastore_config import PostgresDatastoreConfig

        fields: Dict[str, Callable[[Any], None]] = {
            "access": lambda n : setattr(self, 'access', n.get_enum_value(Datastore_access)),
            "builtIn": lambda n : setattr(self, 'built_in', n.get_bool_value()),
            "config": lambda n : setattr(self, 'config', n.get_object_value(Datastore_config)),
            "id": lambda n : setattr(self, 'id', n.get_int_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "owner": lambda n : setattr(self, 'owner', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(Datastore_type)),
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
        writer.write_enum_value("access", self.access)
        writer.write_bool_value("builtIn", self.built_in)
        writer.write_object_value("config", self.config)
        writer.write_int_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_str_value("owner", self.owner)
        writer.write_enum_value("type", self.type)
        writer.write_additional_data_value(self.additional_data)
    
    from kiota_abstractions.serialization import ComposedTypeWrapper

    @dataclass
    class Datastore_config(ComposedTypeWrapper, Parsable):
        from kiota_abstractions.serialization import ComposedTypeWrapper

        """
        Composed type wrapper for classes ElasticsearchDatastoreConfig, PostgresDatastoreConfig
        """
        @staticmethod
        def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> Datastore_config:
            """
            Creates a new instance of the appropriate class based on discriminator value
            param parse_node: The parse node to use to read the discriminator value and create the object
            Returns: Datastore_config
            """
            if not parse_node:
                raise TypeError("parse_node cannot be null.")
            try:
                mapping_value = parse_node.get_child_node("").get_str_value()
            except AttributeError:
                mapping_value = None
            result = Datastore_config()
            if mapping_value and mapping_value.casefold() == "ElasticsearchDatastoreConfig".casefold():
                result.elasticsearch_datastore_config = ElasticsearchDatastoreConfig()
            elif mapping_value and mapping_value.casefold() == "PostgresDatastoreConfig".casefold():
                result.postgres_datastore_config = PostgresDatastoreConfig()
            return result
        
        def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
            """
            The deserialization information for the current model
            Returns: Dict[str, Callable[[ParseNode], None]]
            """
            if self.elasticsearch_datastore_config:
                return self.elasticsearch_datastore_config.get_field_deserializers()
            if self.postgres_datastore_config:
                return self.postgres_datastore_config.get_field_deserializers()
            return {}
        
        def serialize(self,writer: SerializationWriter) -> None:
            """
            Serializes information the current object
            param writer: Serialization writer to use to serialize this model
            Returns: None
            """
            if not writer:
                raise TypeError("writer cannot be null.")
            if self.elasticsearch_datastore_config:
                writer.write_object_value(None, self.elasticsearch_datastore_config)
            elif self.postgres_datastore_config:
                writer.write_object_value(None, self.postgres_datastore_config)
        
    

