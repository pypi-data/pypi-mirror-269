"""Classes and functions to convert between source and internal models of a project.
"""
from operator import itemgetter
from treelib import Tree
from typing import Union, List, Sized, Dict
import tableauserverclient as TSC
from loguru import logger

from TableauConMan.converters.converter import Converter
from TableauConMan.assets.project_asset import Project
from TableauConMan.sources.sources import Source
from TableauConMan.converters.permission_rule_converter import PermissionRuleConverter
from TableauConMan.assets.permission_rule_asset import PermissionRule
import TableauConMan.config.plan_options as options


class ProjectConverter(Converter):
    """Methods for converting between a TSC ProjectItem and TableauConMan Project asset"""

    def __init__(self, source: Source) -> None:
        """Including in the a Source on init to control item filtering

        :param source: Only using ServerSource, but kept at the abstract level
        """
        self.source: Source = source

    @property
    def project_path_id_map(self):
        """Maps the project_path property to the project_id property

        :return: A dict of project_path and project_id
        """
        return self._get_project_path_id_map()

    def convert_to_asset(self, source_item: Union[TSC.ProjectItem, dict]) -> Project:
        """Acts as a method factory to convert from the passed source

        :param item: Should be a project representation from the source.
        :raises TypeError: Will raise an error is there are no methods for the source_type
        :return: Returns a project item converted to the internal asset model.
        """
        converted_asset = None

        if self.source.source_type == "server":
            converted_asset = self.server_to_asset(source_item)
        elif self.source.source_type == "specification":
            converted_asset = self.specification_to_asset(source_item)
        else:
            raise TypeError(
                f"The source_type of {self.source.source_type} is not supported."
            )

        return converted_asset

    def convert_to_source(self, asset: Project) -> Union[TSC.ProjectItem, dict]:
        """Acts as a method factory to convert to the passed source

        :param item: Should be an internal project model
        :raises TypeError: Will raise an error is there are no methods for the source_type
        :return: Returns a source specific project item converted from the internal asset model.
        """
        converted_item = None
        if self.source.source_type == "server":
            converted_item = self.asset_to_server(asset)
        elif self.source.source_type == "specification":
            converted_item = self.asset_to_specification(asset)
        else:
            raise TypeError(
                f"The source_type of {self.source.source_type} is not supported."
            )

        return converted_item

    def asset_to_server(self, project_asset: Project) -> TSC.ProjectItem:
        """Converts a Project asset to a TSC.ProjectItem

        :param project_asset: The project asset to be converted
        :return: The TSC.ProjectItem representation of the project asset
        """
        server_project_item = TSC.ProjectItem(
            name=project_asset.project_name,
            description=project_asset.description,
            content_permissions=project_asset.content_permissions,
            parent_id=self._get_project_parent_id(
                project_asset.project_path, self.project_path_id_map
            ),
        )

        server_project_item._id = project_asset.project_id
        if options.INCLUDE_ASSET_PERMISSIONS and project_asset.manage_permissions:
            rule_converter = PermissionRuleConverter(self.source)

            for rule in project_asset.permission_set:
                if (
                    rule.asset_type
                    not in PermissionRule.PermissionAssetTypes._value2member_map_
                ):
                    continue
                rule_item = rule_converter.asset_to_server(rule)

                item_asset_rule_name = rule_converter._get_project_permission_name(
                    rule.asset_type
                )
                item_asset_rule_object = getattr(
                    server_project_item, item_asset_rule_name
                )
                if item_asset_rule_object is None:
                    setattr(
                        server_project_item, item_asset_rule_name, list([rule_item])
                    )
                else:
                    item_asset_rule_object.append(rule_item)

        return server_project_item

    def asset_to_specification(self, project_asset: Project) -> dict:
        """Converts a Project asset to a project Specification dict

        :param project_asset: The project asset to be converted
        :return: The Specification dict representation of the project asset
        """
        specification_project_item = dict(
            {
                "project_name": project_asset.project_name,
                "project_path": project_asset.project_path,
                "description": project_asset.description,
                "content_permissions": project_asset.content_permissions,
                "permission_set": [],
            }
        )

        if options.INCLUDE_ASSET_PERMISSIONS and project_asset.manage_permissions:
            rule_converter = PermissionRuleConverter(self.source)

            for rule in project_asset.permission_set:
                rule_item = rule_converter.asset_to_specification(rule)

                specification_permission_set: List[
                    Dict
                ] = specification_project_item.get("permission_set")
                if len(specification_permission_set) > 0:
                    set_rule: Dict = next(
                        item
                        for item in specification_permission_set
                        if (item.get("group_name") or item.get("user_name"))
                        == (rule_item.get("group_name") or rule_item.get("user_name"))
                    ).get("permission_rule")
                    set_rule.update(rule_item.get("permission_rule"))
                else:
                    specification_permission_set.append(rule_item)

        return specification_project_item

    def server_to_asset(self, project_item: TSC.ProjectItem) -> Project:
        """Converts a TSC.ProjectItem to a Project asset

        :param project_item: The TSC.ProjectItem to be converted
        :return: The Project asset representation of the TSC.ProjectItem
        """
        asset_project = Project(
            project_id=project_item.id,
            project_path=self._get_project_path(
                project_item.id, self.project_path_id_map
            ),
            project_name=project_item.name,
            description=project_item.description,
            content_permissions=project_item.content_permissions,
            parent_content_permissions=self._get_server_content_permissions(
                project_item.parent_id
            ),
            project_parent_id=project_item.parent_id,
        )

        if options.INCLUDE_ASSET_PERMISSIONS and asset_project.manage_permissions:
            rule_converter = PermissionRuleConverter(self.source)

            logger.debug(f"Getting Permissions for: {project_item.name}")

            for permission_asset in PermissionRule.PermissionAssetTypes:
                with self.source.connect():
                    populate_method = rule_converter._get_project_permission_method(
                        permission_asset.value, "populate"
                    )

                    populate_method(project_item)

                    permission_object = rule_converter._get_project_permission_object(
                        permission_asset.value, project_item
                    )

                    if permission_object is not None:
                        for rule in permission_object():
                            rule_item = rule_converter.server_to_asset(
                                rule, permission_asset.value
                            )

                            asset_project.permission_set.append(rule_item)
            asset_project.permission_set.sort(key=lambda item: item.specification_id)

        return asset_project

    def specification_to_asset(self, project_specification: dict) -> Project:
        """Converts a Specification dict to a Project asset

        :param project_specification: The Specification dict to be converted
        :return: The Project asset representation of the Specification dict
        """
        asset_project = Project(
            project_id="",
            project_name=project_specification.get("project_name"),
            project_path=project_specification.get("project_path"),
            description=project_specification.get("description"),
            content_permissions=project_specification.get("content_permissions"),
            project_parent_id="",
            parent_content_permissions=self._get_specification_parent_content_permissions(
                project_specification.get("project_path")
            ),
        )

        if options.INCLUDE_ASSET_PERMISSIONS and asset_project.manage_permissions:
            rule_converter = PermissionRuleConverter(self.source)

            logger.debug(f"Getting Permissions for: {asset_project.project_name}")

            permission_set: List[PermissionRule] = list()
            if not project_specification.get("permission_set"):
                asset_project.permission_set = permission_set

            for project_rule in project_specification.get("permission_set"):
                # logger.debug(f"Processing permission rule: {project_rule}")
                for asset_rule in project_rule.get("permission_rule").keys():
                    if (
                        asset_rule
                        not in PermissionRule.PermissionAssetTypes._value2member_map_
                    ):
                        continue
                    # logger.debug(f"Processing Rule: {asset_rule}")
                    permission_rule_asset = rule_converter.specification_to_asset(
                        project_rule, asset_rule
                    )

                    permission_set.append(permission_rule_asset)
                    # logger.debug(f"Added Rule: {permission_set}")

            asset_project.permission_set = permission_set

            asset_project.permission_set.sort(key=lambda item: item.specification_id)

        # logger.debug(f"Converted {project_specification} to {asset_project}")

        return asset_project

    @staticmethod
    def _get_project_path(project_item_id: str, project_path_id_map: dict) -> str:
        """Retrieves the project_path for a TSC.ProjectItem project_id

        :param project_item: The TSC.ProjectItem id to get the project_path for
        :param project_path_id_map: A dict of project_path and project_id
        :return: The project_path for the given TSC.ProjectItem
        """
        project_item_path = list(
            filter(
                lambda x: project_path_id_map[x] == project_item_id,
                project_path_id_map,
            )
        )[0]

        return project_item_path

    @staticmethod
    def _get_project_parent_id(project_path: str, project_path_id_map: dict):
        """Retrieves the project_id for project one level up from a given project_path

        :param project_path: A string representing the project_path of a project
        :param project_path_id_map: A dict of project_path and project_id
        :return: A project_id of the project one level up in the project_path
        """
        project_parent_path_end = project_path.rfind("/")
        # A top level project will not have a '/' in the path

        if project_parent_path_end == -1:
            project_parent_path = project_path
            parent_project_id = None
        else:
            project_parent_path = project_path[0:project_parent_path_end]
            parent_project_id = project_path_id_map.get(project_parent_path)

        return parent_project_id

    def _get_server_content_permissions(self, project_id: str) -> str:
        """Retrieves a mapping of project_id and content_permissions

        :return: A dict of project_id and content_permissions
        """
        project_item_list = self.source.get_assets("projects")

        item_content_permission = next(
            (
                item.content_permissions
                for item in project_item_list
                if item.id == project_id
            ),
            "",
        )

        return item_content_permission

    def _get_specification_parent_content_permissions(self, project_path: str) -> str:
        """Retrieves a mapping of project_path and content_permissions

        :return: A content_permissions
        """
        project_item_list = self.source.get_assets("projects")

        project_parent_path_end = project_path.rfind("/")

        if project_parent_path_end == -1:
            project_parent_path = ""
        else:
            project_parent_path = project_path[0:project_parent_path_end]

        item_content_permission = next(
            (
                item.get("content_permissions")
                for item in project_item_list
                if item.get("project_path") == project_parent_path
            ),
            "",
        )

        return item_content_permission

    def _get_project_path_id_map(self):
        """Retrieves a mapping of project_path and project_id

        :return: A dict of project_path and project_id
        """
        project_item_list = self.source.get_assets("projects")

        project_tree = self._parse_projects_to_tree(project_item_list)

        project_path_dict = {}

        for project in project_item_list:
            nodes = list(project_tree.rsearch(project.id))
            nodes.reverse()
            node_path = "/".join(
                [project_tree.get_node(node).data for node in nodes[1:]]
            )
            project_path_dict[node_path] = project.id

        return project_path_dict

    @staticmethod
    def _parse_projects_to_tree(project_item_list):
        """Constructs a node tree based on project_id and parent_id from TSC.ProjectItems

        :param project_item_list: A list of TSC.ProjectItems, should be a full server list for complete coverage
        :return: A tree object that can be searched for for project_id and project_name
        """
        tree = Tree()
        tree.create_node("tableau", "tableau", data="tableau")

        list_root = []
        for project in project_item_list:
            # logger.debug(project)
            if project.parent_id is None:  # not in project.keys()
                tree.create_node(
                    project.id, project.id, parent="tableau", data=project.name
                )
                list_root.append(project_item_list.index(project))

        # logger.debug(project_item_list)

        index_list = list(set(range(len(project_item_list))).difference(list_root))

        if len(index_list) > 0:
            project_list = list()
            project_subset = itemgetter(*index_list)(project_item_list)
            if len(index_list) == 1:
                project_list.append(project_subset)
            else:
                project_list.extend(project_subset)

            while len(index_list) > 0:
                remove_index = list()
                for index, curr_project in enumerate(project_list):
                    parent_project_id = curr_project.parent_id
                    child_project_id = curr_project.id
                    child_name = curr_project.name
                    if tree.get_node(parent_project_id) is not None:
                        tree.create_node(
                            child_project_id,
                            child_project_id,
                            parent=parent_project_id,
                            data=child_name,
                        )
                        remove_index.append(index)

                index_list = list(
                    set(range(len(project_list))).difference(remove_index)
                )
                if len(index_list) > 0:
                    project_list = list(itemgetter(*index_list)(project_list))
        return tree
