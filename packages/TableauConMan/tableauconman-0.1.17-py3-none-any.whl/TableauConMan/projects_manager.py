import os
import hashlib
import json
from typing import Optional
from TableauConMan.assets_manager import AssetsManager
from TableauConMan.helpers import utils
from operator import itemgetter
from treelib import Tree
import tableauserverclient as TSC
from loguru import logger


class ProjectsManager(AssetsManager):
    """
    Initialize the ProjectsManager object.

    :param plan: The plan object specifying the target and reference servers.
    """

    class PermissionAssets:
        Workbook = "workbook"
        Project = "project"
        Datasource = "datasource"
        Flow = "flow"
        Lens = "lens"
        Datarole = "datarole"
        Metric = "metric"

    VALID_PERMISSION_ASSETS = [
        PermissionAssets.Datasource,
        PermissionAssets.Workbook,
        PermissionAssets.Project,
        PermissionAssets.Flow,
        PermissionAssets.Lens,
        PermissionAssets.Datarole,
        PermissionAssets.Metric,
    ]

    def __init__(self, plan) -> None:
        """

        :param plan:
        """
        AssetsManager.__init__(self, plan)
        self.target_projects: Optional[list[TSC.ProjectItem]] = None
        self.target_projects_list: Optional[list] = None
        self.target_project_paths_list: Optional[list] = None
        self.reference_projects: Optional[list[TSC.ProjectItem]] = None
        self.reference_projects_list: Optional[list] = None
        self.reference_project_paths_list: Optional[list] = None

    def populate_projects(self):
        """
        Use object properties to get a comparable list of workbooks from the source and reference
        """
        project_options = self.get_project_options()
        raw_target_projects, raw_target_projects_list = self.generate_server_list(
            self.plan.target,
            self.AssetType.Projects,
        )

        raw_target_project_paths_list = self.get_project_paths(raw_target_projects)

        spec = self.plan.reference

        spec.projects

        # logger.debug(spec.projects)

        reference_projects_list = list(x.get("project_name") for x in spec.projects)
        reference_project_paths_list = list(
            x.get("project_path") for x in spec.projects
        )

        if project_options.get("manage_only_spec_projects"):
            target_project_paths_list_filtered = {
                key: value
                for key, value in raw_target_project_paths_list.items()
                if key in reference_project_paths_list
            }  # {k:v for (k,v) in d.items() if filter_string in k}

            logger.debug(
                f"Filters target Project paths: {target_project_paths_list_filtered}"
            )

            target_projects_filtered = utils.get_filtered_item_list(
                raw_target_projects, target_project_paths_list_filtered.values(), "id"
            )

            logger.debug(f"Filtered target Projects: {target_projects_filtered}")

            target_projects_list_filtered = [x.name for x in target_projects_filtered]

            logger.debug(
                f"Filtered target Project list: {target_projects_list_filtered}"
            )

            target_projects = target_projects_filtered
            target_projects_list = target_projects_list_filtered
            target_project_paths_list = target_project_paths_list_filtered

        else:
            target_projects = raw_target_projects
            target_projects_list = raw_target_projects_list
            target_project_paths_list = raw_target_project_paths_list

        self.target_projects = target_projects
        self.target_projects_list = target_projects_list
        self.target_project_paths_list = target_project_paths_list

        self.reference_projects_list = reference_projects_list
        self.reference_project_paths_list = reference_project_paths_list

    def populate_users_and_groups(self):
        with self.plan.target.connect():
            self.target_users = list(TSC.Pager(self.plan.target.server.users))
            self.target_groups = list(TSC.Pager(self.plan.target.server.groups))

    def populate_project_permissions(self):
        project_server = self.plan.target.server.projects
        with self.plan.target.connect():
            for project in self.target_projects:
                for asset_type in self.VALID_PERMISSION_ASSETS:
                    permission_method = self.get_project_permission_method(
                        asset_type, project_server, "populate"
                    )
                    permission_method(project)

                logger.info(f"Project permissions for {project} have been populated")

    def populate_permission_capabilities(self):
        (
            server_capabilities_list,
            server_capabilities,
        ) = self.get_server_capabilities_list()

        spec_capabilities_list, spec_capabilities = self.get_spec_capabilities_list()

        self.target_project_capabilities = server_capabilities
        self.target_project_capabilities_list = server_capabilities_list
        self.reference_project_capabilities = spec_capabilities
        self.reference_project_capabilities_list = spec_capabilities_list

        # logger.debug(f"Target Capabilities: {server_capabilities}")
        # logger.debug(f"Reference Capabilities: {spec_capabilities}")

    def generate_server_project_schema(self):
        raw_target_projects, raw_target_projects_list = self.generate_server_list(
            self.plan.target,
            self.AssetType.Projects,
        )

        raw_target_project_paths_list = self.get_project_paths(raw_target_projects)

        projects = dict({"projects": []})

        permission_template_list = list()

        for project in raw_target_projects:
            project_path = self.get_project_item_path(
                project, raw_target_project_paths_list
            )

            permission_set, capabilities = self.get_project_item_permission_set(project)

            permission_template_list.extend(capabilities)

            project_schema = dict(
                {
                    "project_name": project.name,
                    "project_path": project_path,
                    "project_id": project.id,
                    "description": project.description,
                    "content_permissions": project.content_permissions,
                    "permission_set": permission_set,
                }
            )

            projects.get("projects").append(project_schema)

        # logger.debug(f"Permission Template List: {permission_template_list}")

        unique_permission_templates = list(
            {
                v.get("permission_template_id"): v for v in permission_template_list
            }.values()
        )

        # logger.debug(f"Unique Permission Templates: {unique_permission_templates}")

        permission_templates = dict(
            {"permission_templates": unique_permission_templates}
        )

        return projects, permission_templates

    def get_project_item_path(self, project_item, project_path_map):
        project_path = list(
            filter(
                lambda x: project_path_map[x] == project_item.id,
                project_path_map,
            )
        )[0]
        return project_path

    def generate_server_permission_templates_schema(self, permission_template_list):
        pass

    def get_project_item_permission_set(self, project_item):
        self.populate_users_and_groups()

        server_users = self.target_users
        server_groups = self.target_groups

        permission_set = list()  # dict({"permission_set": []})

        with self.plan.target.connect():
            for asset_type in self.VALID_PERMISSION_ASSETS:
                permission_method = self.get_project_permission_method(
                    asset_type, self.plan.target.server.projects, "populate"
                )
                permission_method(project_item)
                permission_object = self.get_project_permission_object(
                    asset_type, project_item
                )
                # permission_list = permission_set.get("permission_set")

                # logger.debug(f"Permission Object: {permission_object}")
                for permission in permission_object:
                    # permission_rule = dict()
                    if permission.grantee.tag_name == "user":
                        user_item = list(
                            filter(
                                lambda x: x.id == permission.grantee.id,
                                server_users,
                            )
                        )[0]

                        grantee_name = user_item.name
                        grantee_key = "user_name"

                    elif permission.grantee.tag_name == "group":
                        group_item = list(
                            filter(
                                lambda x: x.id == permission.grantee.id,
                                server_groups,
                            )
                        )[0]
                        grantee_name = group_item.name
                        grantee_key = "group_name"

                    # permission_rule.update({asset_type: permission.capabilities})

                    permission_rule = dict(
                        {
                            grantee_key: grantee_name,
                            "permission_list": {asset_type: permission.capabilities},
                        }
                    )

                    existing_grantee = next(
                        (
                            item
                            for item in permission_set
                            if item.get(grantee_key) == grantee_name
                        ),
                        None,
                    )

                    if existing_grantee:
                        existing_grantee.get("permission_list").update(
                            {asset_type: permission.capabilities}
                        )
                    else:
                        permission_set.append(permission_rule)

        capabilities = list()

        for rule in permission_set:
            rule_list = rule.get("permission_list").copy()
            rule_id = hashlib.md5(
                json.dumps(rule_list, sort_keys=True).encode("utf-8")
            ).hexdigest()
            rule.update({"permission_template_id": rule_id})

            rule_list.update({"permission_template_id": rule_id})

            capabilities.append(rule_list)

            rule.pop("permission_list")

        """logger.debug(
            f"Project: {project_item.name} |  Permission Rules: {permission_set}"
        )"""

        return permission_set, capabilities

    def get_inherited_grantees(self, project):
        inherited_grantees = []
        for permission in project.permissions:
            # logger.debug(f"Permission Capabilities:{permission.capabilities} ")
            if permission.capabilities.get("InheritedProjectLeader") is not None:
                if permission.capabilities.get("InheritedProjectLeader") == "Allow":
                    inherited_grantees.append(permission.grantee.id)

        return inherited_grantees

    def get_server_capabilities_list(self):
        logger.info("Processing Capabilities")
        server = self.plan.target.server
        server_projects = self.target_projects
        server_users = self.target_users
        server_groups = self.target_groups
        project_options = self.get_project_options()  # Filter based on options

        server_project_path_map = self.target_project_paths_list

        server_capabilities_list = list()
        server_capabilities_dict_list = list()

        for project in server_projects:
            project_path = list(
                filter(
                    lambda x: server_project_path_map[x] == project.id,
                    server_project_path_map,
                )
            )[0]
            # project_path_dict = dict({project_path: list()})
            # server_capabilities_list.append(project_path_dict)
            """logger.debug(
                f"Capabilities Project: {project} | Path: {project_path} | capabilities list: {server_capabilities_list} "
            )"""
            """logger.warning(
                f"Project {project.name} | Content Permissions: {project.content_permissions} | Project Parent ID: {project.parent_id}"
            )"""
            if project.parent_id:
                parent_project_content_permissions = list(
                    filter(lambda x: project.parent_id == x.id, server_projects)
                )[0].content_permissions
            else:
                parent_project_content_permissions = "None"
            """logger.debug(
                f"Project Content Permission:{project.content_permissions} | Parent Project Content Permissions: {parent_project_content_permissions} "
            )"""
            if (
                project.content_permissions != project.ContentPermissions.ManagedByOwner
                and (
                    project.content_permissions
                    == project.ContentPermissions.LockedToProject
                    and parent_project_content_permissions
                    != project.ContentPermissions.LockedToProject
                )
                or project.content_permissions
                == project.ContentPermissions.LockedToProjectWithoutNested
            ):
                # Check for inheritance and filer out permissions
                with self.plan.target.connect():
                    inherited_grantees = self.get_inherited_grantees(project)
                    for asset_type in self.VALID_PERMISSION_ASSETS:
                        permission_object = self.get_project_permission_object(
                            asset_type, project
                        )
                        for permission in permission_object:
                            # print(project.id,permission.grantee.tag_name,permission.capabilities)
                            if permission.grantee.id not in inherited_grantees:
                                if permission.grantee.tag_name == "user":
                                    user_item = list(
                                        filter(
                                            lambda x: x.id == permission.grantee.id,
                                            server_users,
                                        )
                                    )[0]

                                    grantee_name = user_item.name
                                elif permission.grantee.tag_name == "group":
                                    group_item = list(
                                        filter(
                                            lambda x: x.id == permission.grantee.id,
                                            server_groups,
                                        )
                                    )[0]
                                    grantee_name = group_item.name

                                for capability in permission.capabilities.keys():
                                    server_capability_detail = {}

                                    server_capability_detail.update(
                                        {
                                            "project_path": project_path,
                                            "grantee_type": permission.grantee.tag_name,
                                            "grantee_name": grantee_name,
                                            "asset_type": asset_type,
                                            "capability": capability,
                                            "mode": permission.capabilities.get(
                                                capability
                                            ),
                                        }
                                    )

                                    server_capabilities_dict_list.append(
                                        server_capability_detail
                                    )

                                    server_capabilities_list.append(
                                        f"{project_path} | {permission.grantee.tag_name} | {grantee_name} | {asset_type} | {capability} | {permission.capabilities.get(capability)}"
                                    )

        return server_capabilities_list, server_capabilities_dict_list

    def get_spec_capabilities_list(self):
        spec_projects = self.plan.reference.projects
        # spec_projects = list(filter(lambda x: x['project_path'] == 'Pilot/Business Insights', spec_projects))

        spec_permission_templates = self.plan.reference.permission_templates

        # print(spec_permission_templates)

        spec_capabilities_list = list()
        spec_capabilities_dict_list = list()

        for project in spec_projects:
            project_content_permissions = project.get("content_permissions")
            permission_set = project.get("permission_set")
            project_path = project.get("project_path")
            parent_project_path = project_path.split(project.get("project_name"))[
                0
            ].rstrip("/")
            if parent_project_path != "":
                parent_project = list(
                    filter(
                        lambda x: parent_project_path == x.get("project_path"),
                        spec_projects,
                    )
                )[0]
            else:
                parent_project = dict()

            """logger.debug(
                f"Project Parent Path: {parent_project_path} | Project Path: {project_path} | Parent Project: {parent_project}"
            )"""
            parent_project_content_permissions = parent_project.get(
                "content_permissions"
            )
            if (
                permission_set is not None
                and project_content_permissions
                != TSC.ProjectItem.ContentPermissions.ManagedByOwner
                and (
                    project_content_permissions
                    == TSC.ProjectItem.ContentPermissions.LockedToProject
                    and parent_project_content_permissions
                    != TSC.ProjectItem.ContentPermissions.LockedToProject
                )
                or project_content_permissions
                == TSC.ProjectItem.ContentPermissions.LockedToProjectWithoutNested
            ):
                # print(project['permission_set'])
                for permission in permission_set:
                    if permission.get("group_name") is not None:
                        grantee_type = "group"
                        grantee_name = permission.get("group_name")
                    elif permission.get("user_name") is not None:
                        grantee_type = "user"
                        grantee_name = permission.get("user_name")
                    # print(permission['permission_rule'])
                    try:
                        permission_template = list(
                            filter(
                                lambda x: x.get("name")
                                == permission.get("permission_rule"),
                                spec_permission_templates,
                            )
                        )[0]
                    except Exception as exc:
                        logger.info(
                            f"Project {project.get('project_path')} does not have a valid permission template: {permission.get('permission_rule')} "
                        )
                        logger.debug(exc)
                    # print(permission_template)
                    for asset_type, capabilities in permission_template.items():
                        # print(asset_type,capabilities, permission['permission_rule'])
                        if (
                            asset_type != "name"
                            and asset_type in self.VALID_PERMISSION_ASSETS
                        ):
                            # print(asset_type,capabilities)
                            for capability, mode in capabilities.items():
                                # print(capability,asset_type[capability])
                                spec_capability_detail = {}

                                spec_capability_detail.update(
                                    {
                                        "project_path": project.get("project_path"),
                                        "grantee_type": grantee_type,
                                        "grantee_name": grantee_name,
                                        "asset_type": asset_type,
                                        "capability": capability,
                                        "mode": mode,
                                    }
                                )

                                # print(server_capability_detail)
                                spec_capabilities_dict_list.append(
                                    spec_capability_detail
                                )
                                spec_capabilities_list.append(
                                    f"{project.get('project_path')} | {grantee_type} | {grantee_name} | {asset_type} | {capability} | {mode}"
                                )

        return spec_capabilities_list, spec_capabilities_dict_list

    def get_project_permission_object(self, asset_type, project):
        if asset_type == self.PermissionAssets.Project:
            permission_object_name = "permissions"
        else:
            permission_object_name = f"default_{asset_type}_permissions"

        permission_object = getattr(project, permission_object_name)

        return permission_object

    def get_project_permission_method(self, asset_type, server_projects, action):
        if asset_type == self.PermissionAssets.Project:
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

        permission_method = getattr(server_projects, permission_method_name)

        return permission_method

    def get_project_changes(self):
        """ """

        common, to_remove, to_add = self.get_changes(
            self.target_project_paths_list, self.reference_project_paths_list
        )

        to_update = list()

        for project in common:
            (
                target_project_content_permission,
                target_project_description,
                reference_project_content_permission,
                reference_project_description,
                target_project_item,
            ) = self.get_project_update_attributes(project)

            if (
                target_project_content_permission
                != reference_project_content_permission
                or target_project_description != reference_project_description
            ):
                to_update.append(project)

        return to_update, to_remove, to_add

    def get_project_update_attributes(self, project_path):
        target_project_id = self.target_project_paths_list.get(project_path)
        target_project_item = utils.get_filtered_item_list(
            self.target_projects, target_project_id, "id"
        )[0]
        target_project_content_permission = target_project_item.content_permissions
        target_project_description = target_project_item.description

        reference_project = utils.get_filtered_dict_list(
            self.plan.reference.projects, project_path, "project_path"
        )[0]

        reference_project_content_permission = reference_project.get(
            "content_permissions"
        )
        reference_project_description = reference_project.get("description")

        return (
            target_project_content_permission,
            target_project_description,
            reference_project_content_permission,
            reference_project_description,
            target_project_item,
        )

    def get_permission_changes(self):
        """ """
        common, to_remove, to_add = self.get_changes(
            self.target_project_capabilities_list,
            self.reference_project_capabilities_list,
        )

        return common, to_remove, to_add

    def get_project_paths(self, project_item_list):
        project_tree = self.parse_projects_to_tree(project_item_list)

        project_path_dict = {}

        for project in project_item_list:
            nodes = list(project_tree.rsearch(project.id))
            nodes.reverse()
            node_path = "/".join(
                [project_tree.get_node(node).data for node in nodes[1:]]
            )
            project_path_dict[node_path] = project.id
            # project_path_dict[project.id] = f"{node_path}"

            # project_json["projects"].append(project_path_dict)

        return project_path_dict

    def parse_projects_to_tree(self, project_item_list):
        tree = Tree()
        tree.create_node("tableau", "tableau", data="tableau")

        list_root = []
        for project in project_item_list:
            if project.parent_id is None:  # not in project.keys()
                tree.create_node(
                    project.id, project.id, parent="tableau", data=project.name
                )
                list_root.append(project_item_list.index(project))

        index_list = list(set(range(len(project_item_list))).difference(list_root))
        # print(f"The projects object {index_list}" )
        """logger.debug(
            f"The index list {index_list} | The project_item_list: {project_item_list} | The list_root: {list_root}"
        )"""
        # logger.debug(f"The project list: {itemgetter(*index_list)(project_item_list)}")
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
                    # print(f"The projects object {curr_project}" )
                    parent_project_id = curr_project.parent_id  # ['@parentProjectId']
                    child_project_id = curr_project.id  # ['@id']
                    child_name = curr_project.name  # ['@name']
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
                    project_list = list(
                        itemgetter(*index_list)(project_list)
                    )  # list(project_list.itemgetter(*index_list)) #
        return tree

    def get_project_parent_id(self, project_path):
        project_parent_path_end = project_path.rfind("/")
        # A top level project will not have a '/' in the path

        """logger.debug(
            f"Project path end: {project_parent_path_end} | Project path {project_path} | target paths: {self.target_project_paths_list}"
        )"""

        if project_parent_path_end == -1:
            project_parent_path = project_path
            parent_project_id = None
        else:
            project_parent_path = project_path[0:project_parent_path_end]
            parent_project_id = self.target_project_paths_list.get(project_parent_path)

        return parent_project_id

    def format_reference_project(self, project_path):
        reference_project = dict()

        parent_project_id = self.get_project_parent_id(project_path)

        project_details = utils.get_filtered_dict_list(
            self.plan.reference.projects, project_path, "project_path"
        )[0]

        project_details.update({"parent_project_id": parent_project_id})

        reference_project = project_details

        # logger.debug(reference_project)

        return reference_project

    def create(self, reference_project):
        new_project = TSC.ProjectItem(
            name=reference_project.get("project_name"),
            content_permissions=reference_project.get("content_permissions"),
            description=reference_project.get("description"),
            parent_id=reference_project.get("parent_project_id"),
        )

        with self.plan.target.connect():
            created_project = self.plan.target.server.projects.create(new_project)

        return created_project

    def get_project_options(self):
        """

        :return:
        """
        project_config = self.plan.asset_options.get("projects")
        project_options = project_config.get("options")
        return project_options

    def update_project(self, project_item):
        with self.plan.target.connect():
            updated_project = self.plan.target.server.projects.update(project_item)

        return updated_project

    def delete(self, project_item):
        with self.plan.target.connect():
            self.plan.target.server.projects.delete(project_item.id)

    def update_permission(self, project_item, asset_type, rules_list):
        source = self.plan.target
        asset_permissions = self.get_project_permission_method(
            asset_type, source.server.projects, "update"
        )

        with source.connect():
            asset_permissions(project_item, rules_list)

        logger.info(f"Project {project_item.name} permissions updated")

    def delete_permission(self, project_item, asset_type, rules_list):
        source = self.plan.target
        asset_permissions = self.get_project_permission_method(
            asset_type, source.server.projects, "delete"
        )

        # logger.debug(f"Project: {project_item} | Rules: {rules_list}")

        with source.connect():
            # try:
            asset_permissions(project_item, rules_list[0])
        # except Exception as exc:
        #     logger.warning(exc)

        logger.info(f"Project {project_item.name} permissions deleted")

    def add(self, to_add_list):
        """ """

        for project in to_add_list:
            reference_project = self.format_reference_project(project)

            created_project = self.create(reference_project)

            logger.info(f"Project {created_project} added.")

    def remove(self, to_remove_list):
        project_options = self.get_project_options()

        # logger.debug(f"Target Project Paths: {self.target_project_paths_list}")

        if not project_options.get("manage_only_spec_projects"):
            for project in to_remove_list:
                project_id = self.target_project_paths_list.get(project)
                project_item = list(
                    filter(lambda x: project_id == x.id, self.target_projects)
                )[0]
                if project_options.get("archive_on_delete"):
                    archive_project = project_options.get("archive_project_path")
                    archive_project_id = self.target_project_paths_list.get(
                        archive_project
                    )
                    # Check for if the project is already in the Archived location
                    if project_item.parent_id != archive_project_id:
                        project_item.parent_id = archive_project_id

                        archived_project = self.update_project(project_item)

                        logger.debug(f"Archived project: {archived_project}")
                else:
                    self.delete(project_item)

                    logger.debug(f"Deleted project: {project_item}")

    def update(self, to_update_list):
        for project in to_update_list:
            (
                target_project_content_permission,
                target_project_description,
                reference_project_content_permission,
                reference_project_description,
                project_item,
            ) = self.get_project_update_attributes(project)

            project_item.content_permissions = reference_project_content_permission
            project_item.description = reference_project_description

            updated_project = self.update_project(project_item)

            logger.debug(f"Updated project: {updated_project}")

    def format_project_permission_rules(
        self, project_path, asset_type, capabilities_list
    ):
        project = project_path

        asset_capabilities_list = utils.get_filtered_dict_list(
            capabilities_list, asset_type, "asset_type"
        )

        logger.debug(
            f"Project {project} Asset: {asset_type} capabilities list: {asset_capabilities_list}"
        )

        grantee_list = list(
            set([x.get("grantee_name") for x in asset_capabilities_list])
        )

        project_asset_grantee_rules = list()

        for grantee in grantee_list:
            grantee_asset_capabilities_list = utils.get_filtered_dict_list(
                asset_capabilities_list, grantee, "grantee_name"
            )

            logger.debug(
                f"Project {project} Asset: {asset_type} Grantee: {grantee} capabilities list: {grantee_asset_capabilities_list}"
            )

            capabilities = dict()
            for capability in grantee_asset_capabilities_list:
                capabilities.update(
                    {
                        getattr(
                            TSC.Permission.Capability,
                            capability.get("capability"),
                        ): getattr(TSC.Permission.Mode, capability.get("mode"))
                    }
                )

            grantee_type = capability.get("grantee_type")
            if grantee_type == "group":
                grantee_item_list = self.target_groups
            elif grantee_type == "user":
                grantee_item_list = self.target_users
            grantee_item = self.get_item_from_list(grantee, grantee_item_list)

            project_asset_grantee_rule = TSC.PermissionsRule(
                grantee=grantee_item, capabilities=capabilities
            )

            project_asset_grantee_rules.append(project_asset_grantee_rule)

        logger.debug(
            f"Project Asset Grantee Rules: {project}-{asset_type}-{project_asset_grantee_rules}"
        )
        return project_asset_grantee_rules

    def format_capability(self, capability_string):
        capability_list = capability_string.split(" | ")
        capability_dict = dict()
        capability_project_path = capability_list[0]
        capability_grantee_type = capability_list[1]
        capability_grantee_name = capability_list[2]
        capability_asset_type = capability_list[3]
        capability = capability_list[4]
        mode = capability_list[5]
        capability_dict.update(
            {
                "project_path": capability_project_path,
                "grantee_type": capability_grantee_type,
                "grantee_name": capability_grantee_name,
                "asset_type": capability_asset_type,
                "capability": capability,
                "mode": mode,
            }
        )

        return capability_dict

    def add_capabilities(self, to_add_list):
        """
        Filter list by project
        Get project item
        Get group items
        get user items
        format rules
        """
        for capability in to_add_list:
            formatted_capability = self.format_capability(capability)
            capability_list = list()
            capability_list.append(formatted_capability)

            logger.debug(f"Formatted capability {formatted_capability}")

            project = formatted_capability.get("project_path")

            project_id = self.target_project_paths_list.get(project)
            project_item = list(
                filter(lambda x: project_id == x.id, self.target_projects)
            )[0]
            asset_type = formatted_capability.get("asset_type")

            project_rules = self.format_project_permission_rules(
                project, asset_type, capability_list
            )

            self.update_permission(project_item, asset_type, project_rules)

    def remove_capabilities(self, to_remove_list):
        for capability in to_remove_list:
            formatted_capability = self.format_capability(capability)
            capability_list = list()
            capability_list.append(formatted_capability)

            logger.debug(f"Formatted capability {formatted_capability}")

            project = formatted_capability.get("project_path")

            project_id = self.target_project_paths_list.get(project)
            project_item = list(
                filter(lambda x: project_id == x.id, self.target_projects)
            )[0]
            asset_type = formatted_capability.get("asset_type")

            project_rules = self.format_project_permission_rules(
                project, asset_type, capability_list
            )

            self.delete_permission(project_item, asset_type, project_rules)
