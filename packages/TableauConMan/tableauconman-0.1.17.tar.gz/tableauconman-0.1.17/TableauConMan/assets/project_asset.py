from dataclasses import dataclass, field
from typing import List

from TableauConMan.assets.asset import Asset
from TableauConMan.assets.permission_rule_asset import PermissionRule
import hashlib
import json


@dataclass
class Project(Asset):
    project_id: str
    project_path: str
    project_parent_id: str
    project_name: str
    description: str
    content_permissions: str
    parent_content_permissions: str
    permission_set: List[PermissionRule] = field(default_factory=list)

    @property
    def manage_permissions(self) -> bool:
        return (
            self.parent_content_permissions != "LockedToProject"
            and self.content_permissions != "ManagedByOwner"
        )

    def update_asset(self, reference_asset: Asset) -> None:
        self.description = reference_asset.description
        self.content_permissions = reference_asset.content_permissions

    @property
    def specification_id(self):
        return hashlib.md5(self.project_path.encode("utf-8")).hexdigest()

    @property
    def update_checksum(self):
        return hashlib.md5(
            (
                self.specification_id
                + self.description
                + self.content_permissions
                + json.dumps(
                    self.permission_set, default=lambda o: o.__dict__, sort_keys=True
                )
            ).encode("utf-8")
        ).hexdigest()

    @property
    def update_value(self):
        return 1
