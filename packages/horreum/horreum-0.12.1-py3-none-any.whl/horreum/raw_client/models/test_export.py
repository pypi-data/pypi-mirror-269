from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .action import Action
    from .experiment_profile import ExperimentProfile
    from .missing_data_rule import MissingDataRule
    from .test import Test
    from .test_export_datastore import TestExport_datastore
    from .test_export_subscriptions import TestExport_subscriptions
    from .variable import Variable

from .test import Test

@dataclass
class TestExport(Test):
    """
    Represents a Test with all associated data used for export/import operations.
    """
    # Array of Actions associated with test
    actions: Optional[List[Action]] = None
    # Datastore associated with test
    datastore: Optional[TestExport_datastore] = None
    # Array of ExperimentProfiles associated with test
    experiments: Optional[List[ExperimentProfile]] = None
    # Array of MissingDataRules associated with test
    missing_data_rules: Optional[List[MissingDataRule]] = None
    # Watcher object associated with test
    subscriptions: Optional[TestExport_subscriptions] = None
    # Array of Variables associated with test
    variables: Optional[List[Variable]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> TestExport:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TestExport
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return TestExport()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        from .action import Action
        from .experiment_profile import ExperimentProfile
        from .missing_data_rule import MissingDataRule
        from .test import Test
        from .test_export_datastore import TestExport_datastore
        from .test_export_subscriptions import TestExport_subscriptions
        from .variable import Variable

        from .action import Action
        from .experiment_profile import ExperimentProfile
        from .missing_data_rule import MissingDataRule
        from .test import Test
        from .test_export_datastore import TestExport_datastore
        from .test_export_subscriptions import TestExport_subscriptions
        from .variable import Variable

        fields: Dict[str, Callable[[Any], None]] = {
            "actions": lambda n : setattr(self, 'actions', n.get_collection_of_object_values(Action)),
            "datastore": lambda n : setattr(self, 'datastore', n.get_object_value(TestExport_datastore)),
            "experiments": lambda n : setattr(self, 'experiments', n.get_collection_of_object_values(ExperimentProfile)),
            "missingDataRules": lambda n : setattr(self, 'missing_data_rules', n.get_collection_of_object_values(MissingDataRule)),
            "subscriptions": lambda n : setattr(self, 'subscriptions', n.get_object_value(TestExport_subscriptions)),
            "variables": lambda n : setattr(self, 'variables', n.get_collection_of_object_values(Variable)),
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
        writer.write_collection_of_object_values("actions", self.actions)
        writer.write_object_value("datastore", self.datastore)
        writer.write_collection_of_object_values("experiments", self.experiments)
        writer.write_collection_of_object_values("missingDataRules", self.missing_data_rules)
        writer.write_object_value("subscriptions", self.subscriptions)
        writer.write_collection_of_object_values("variables", self.variables)
    

