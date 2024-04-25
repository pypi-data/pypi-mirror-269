from typing import Any
from TableauConMan.managers.project_manager import ProjectManager


class AssetManagerFactory:
    @staticmethod
    def get_asset_manager(asset_type: str) -> Any:
        if asset_type == "projects":
            return ProjectManager()
        raise TypeError(f"No manager for the {asset_type} asset_type")
