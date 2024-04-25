from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

@dataclass
class GithubIssueCommentAction(AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: Dict[str, Any] = field(default_factory=dict)

    # The formatter property
    formatter: Optional[str] = None
    # The issue property
    issue: Optional[str] = None
    # The issueUrl property
    issue_url: Optional[str] = None
    # The owner property
    owner: Optional[str] = None
    # The repo property
    repo: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: Optional[ParseNode] = None) -> GithubIssueCommentAction:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: GithubIssueCommentAction
        """
        if not parse_node:
            raise TypeError("parse_node cannot be null.")
        return GithubIssueCommentAction()
    
    def get_field_deserializers(self,) -> Dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: Dict[str, Callable[[ParseNode], None]]
        """
        fields: Dict[str, Callable[[Any], None]] = {
            "formatter": lambda n : setattr(self, 'formatter', n.get_str_value()),
            "issue": lambda n : setattr(self, 'issue', n.get_str_value()),
            "issueUrl": lambda n : setattr(self, 'issue_url', n.get_str_value()),
            "owner": lambda n : setattr(self, 'owner', n.get_str_value()),
            "repo": lambda n : setattr(self, 'repo', n.get_str_value()),
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
        writer.write_str_value("formatter", self.formatter)
        writer.write_str_value("issue", self.issue)
        writer.write_str_value("issueUrl", self.issue_url)
        writer.write_str_value("owner", self.owner)
        writer.write_str_value("repo", self.repo)
        writer.write_additional_data_value(self.additional_data)
    

