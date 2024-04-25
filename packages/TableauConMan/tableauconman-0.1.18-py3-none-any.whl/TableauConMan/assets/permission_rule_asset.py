from dataclasses import dataclass
from typing import List
from enum import Enum
from TableauConMan.assets.asset import Asset
import hashlib
import json


@dataclass
class PermissionRule(Asset):
    class PermissionAssetTypes(Enum):
        Project = "project"
        Workbook = "workbook"
        Datasource = "datasource"

    asset_type: str
    grantee_type: str
    grantee_name: str
    capabilities: dict

    @property
    def specification_id(self):
        return hashlib.md5(
            (self.asset_type + self.grantee_type + self.grantee_name).encode("utf-8")
        ).hexdigest()

    @property
    def update_checksum(self):
        return hashlib.md5(
            (
                self.specification_id + json.dumps(self.capabilities, sort_keys=True)
            ).encode("utf-8")
        ).hexdigest()

    @property
    def update_value(self):
        return 1
