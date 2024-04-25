"""Classes and functions to convert between source and internal models of a project permission rule.
"""
from typing import List
import tableauserverclient as TSC


from TableauConMan.converters.converter import Converter
from TableauConMan.assets.permission_rule_asset import PermissionRule
from TableauConMan.sources.sources import Source
from TableauConMan.sources.server_source import ServerSource


class PermissionRuleConverter(Converter):
    """Methods for converting between a TSC ProjectItem and ConMan ProjectSpec"""

    def __init__(self, source: Source) -> None:
        """Including in the a Source on init to control item filtering

        :param source: Only using ServerSource, but kept at the abstract level
        """
        self.source: Source = source

    def convert_to_asset(
        self, source_item: TSC.PermissionsRule or dict, asset_type: str
    ) -> PermissionRule:
        """_summary_

        :param source_item: _description_
        :return: _description_
        """
        converted_asset = None

        if isinstance(source_item, TSC.PermissionsRule):
            converted_asset = self.server_to_asset(source_item, asset_type)
        else:
            converted_asset = self.specification_to_asset(source_item, asset_type)

        return converted_asset

    def convert_to_source(self, asset: PermissionRule) -> TSC.PermissionsRule or dict:
        """_summary_

        :param asset: _description_
        :return: _description_
        """
        converted_item = None

        if isinstance(self.source, ServerSource):
            converted_item = self.asset_to_server(asset)
        else:
            converted_item = self.asset_to_specification(asset)

        return converted_item

    def asset_to_server(
        self, permission_rule_asset: PermissionRule
    ) -> TSC.PermissionsRule:
        """
        convert grantee name to TSC id

        """
        server_permission_rule = TSC.PermissionsRule(
            grantee=self._get_grantee_item(
                permission_rule_asset.grantee_name, permission_rule_asset.grantee_type
            ),
            capabilities=permission_rule_asset.capabilities,
        )

        return server_permission_rule

    def asset_to_specification(self, permission_rule_asset: PermissionRule) -> dict:
        """_summary_

        :param permission_rule_asset: _description_
        :return: _description_
        """
        specification_permission_rule = dict(
            {
                permission_rule_asset.grantee_type
                + "_name": permission_rule_asset.grantee_name,
                "permission_rule": dict(
                    {
                        permission_rule_asset.asset_type: permission_rule_asset.capabilities
                    }
                ),
            }
        )

        return specification_permission_rule

    def server_to_asset(
        self, permission_rule_item: TSC.PermissionsRule, asset_type: str
    ) -> PermissionRule:
        """_summary_

        :param permission_rule_item: _description_
        :param asset_type: _description_
        :return: _description_
        """
        permission_rule_asset = PermissionRule(
            asset_type=asset_type,
            grantee_name=self._get_grantee_name(
                permission_rule_item.grantee.id, permission_rule_item.grantee.tag_name
            ),
            grantee_type=permission_rule_item.grantee.tag_name,
            capabilities=permission_rule_item.capabilities,
        )

        return permission_rule_asset

    def specification_to_asset(
        self, specification_permission_rule: dict, asset_type: str
    ) -> PermissionRule:
        """_summary_

        :param specification_permission_rule: _description_
        :param asset_type: _description_
        :return: _description_
        """
        permission_rule_asset = PermissionRule(
            asset_type=asset_type,
            grantee_name=specification_permission_rule.get("group_name")
            or specification_permission_rule.get("user_name"),
            grantee_type=next(
                item[: len(item) - 5]
                for item in specification_permission_rule.keys()
                if item[-5:] == "_name"
            ),
            capabilities=specification_permission_rule.get("permission_rule", {}).get(
                asset_type
            ),
        )

        return permission_rule_asset

    def _get_grantee_item(self, grantee_name: str, grantee_type: str):
        """summary

        :param grantee_name: _description_
        :param grantee_type: _description_
        :raises TypeError: _description_
        :return: _description_
        """

        if grantee_type == "user":
            grantee_item_list = self.source.get_assets("users")
        elif grantee_type == "group":
            grantee_item_list = self.source.get_assets("groups")
        else:
            raise TypeError

        grantee_item = next(
            item for item in grantee_item_list if item.name == grantee_name
        )

        return grantee_item

    def _get_grantee_name(self, grantee_id: str, grantee_type: str) -> str:
        """summary

        :param grantee_name: _description_
        :param grantee_type: _description_
        :raises TypeError: _description_
        :return: _description_
        """

        if grantee_type == "user":
            grantee_item_list = self.source.get_assets("users")
        elif grantee_type == "group":
            grantee_item_list = self.source.get_assets("groups")
        else:
            raise TypeError

        grantee_name = next(
            item.name for item in grantee_item_list if item.id == grantee_id
        )

        return grantee_name

    def _convert_capabilities(self, asset_capabilities: List[dict]) -> dict:
        """_summary_

        :param asset_capabilities: _description_
        :return: _description_
        """
        capabilities_dict = dict(
            {item.capability: item.mode for item in asset_capabilities}
        )

        return capabilities_dict

    def _get_project_permission_object(self, asset_type, project_item):
        """_summary_

        :param asset_type: _description_
        :param project_item: _description_
        :return: _description_
        """
        if asset_type == "project":
            permission_object_name = "_permissions"
        else:
            permission_object_name = f"_default_{asset_type}_permissions"

        permission_object = getattr(project_item, permission_object_name)

        return permission_object

    def _get_project_permission_name(self, asset_type):
        """_summary_

        :param asset_type: _description_
        :return: _description_
        """
        if asset_type == "project":
            permission_object_name = "_permissions"
        else:
            permission_object_name = f"_default_{asset_type}_permissions"

        return permission_object_name

    def _get_project_permission_method(self, asset_type, action):
        """_summary_

        :param asset_type: _description_
        :param action: _description_
        :return: _description_
        """
        if asset_type == "project":
            if action == "update":
                permission_method_name = "update_permission"
            elif action == "delete":
                permission_method_name = "delete_permission"
            elif action == "populate":
                permission_method_name = "populate_permissions"
        else:
            if action == "update":
                permission_method_name = f"update_{asset_type}_default_permissions"
            elif action == "delete":
                permission_method_name = f"delete_{asset_type}_default_permissions"
            elif action == "populate":
                permission_method_name = f"populate_{asset_type}_default_permissions"

        permission_method = getattr(self.source.server.projects, permission_method_name)

        return permission_method
