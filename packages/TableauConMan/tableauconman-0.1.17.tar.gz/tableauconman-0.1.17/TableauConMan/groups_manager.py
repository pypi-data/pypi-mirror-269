from typing import Optional
from TableauConMan.assets_manager import AssetsManager
from TableauConMan.helpers import utils
import tableauserverclient as TSC
from loguru import logger


class GroupsManager(AssetsManager):
    """

    :class: `GroupsManager` is a subclass of `AssetsManager` that provides functionality for managing groups in a Tableau Server. It includes methods for populating groups, generating a
    * server list, getting group changes, deleting a group, creating a group, adding and removing users from a group, and updating group membership.

    :class: `GroupsManager` inherits from `AssetsManager`. The `AssetsManager` class provides basic functionality for managing assets in a Tableau Server, such as workbooks, data sources
    *, and projects.

    :param plan: A Plan object that contains information about the action to be performed.

    :ivar target_groups: A list of `TSC.GroupItem` objects representing the groups in the target server.
    :ivar target_groups_list: A list of group names in the target server.
    :ivar target_group_memberships_list: A list of dictionaries representing group memberships in the target server.
    :ivar reference_groups: A list of `TSC.GroupItem` objects representing the groups in the reference server.
    :ivar reference_groups_list: A list of group names in the reference server.
    :ivar reference_group_memberships_list: A list of dictionaries representing group memberships in the reference server.
    :ivar target_users: A list of user names in the target server.
    :ivar reference_users: A list of user names in the reference server.

    Methods:

    .. method:: populate_groups()

       Use object properties to get a comparable list of groups from the source and reference servers.

    .. method:: populate_users()

       Use object properties to get a list of users from the target server.

    .. method:: _generate_server_list(source, asset_type, filter=None)

       Generate a list of assets from a server.

       :param source: The server to generate the list from.
       :param asset_type: The type of asset to generate the list for.
       :param filter: Optional. A filter to apply to the asset list.

       :return: A tuple containing the list of assets and the list of asset names.

    .. method:: get_group_changes()

       Get the changes between the target and reference groups.

       :return: A tuple containing the groups to be added, the groups to be removed, and the groups to be updated.

    .. method:: get_group_memberships(group_name)

       Get the memberships of a specific group.

       :param group_name: The name of the group.

       :return: A tuple containing the reference memberships and the target memberships.

    .. method:: delete_group(group)

       Delete a group from the target server.

       :param group: The group to delete.

    .. method:: create(group_name)

       Create a new group in the target server.

       :param group_name: The name of the group to create.

       :return: The created group.

    .. method:: add_user(group_item, user_item)

       Add a user to a group.

       :param group_item: The group to add the user to.
       :param user_item: The user to add to the group.

    .. method:: remove_user(group_item, user_item)

       Remove a user from a group.

       :param group_item: The group to remove the user from.
       :param user_item: The user to remove from the group.

    .. method:: update_group_membership(group_item)

       Update the membership of a group.

       :param group_item: The group to update the membership of.

    .. method:: add(list_to_add)

       Add groups to the target server.

       :param list_to_add: A list of group names to add.

    .. method:: remove(remove_list)

       Remove groups from the target server.

       :param remove_list: A list of group names to remove.

    .. method:: update(update_list)

       Update groups in the target server.

       :param update_list: A list of group names to update.

    """

    def __init__(self, plan) -> None:
        """

        :param plan:
        """
        AssetsManager.__init__(self, plan)
        self.target_groups: Optional[list[TSC.GroupItem]] = None
        self.target_groups_list: Optional[list] = None
        self.target_group_memberships_list: Optional[list] = None
        self.reference_groups: Optional[list[TSC.GroupItem]] = None
        self.reference_groups_list: Optional[list] = None
        self.reference_group_memberships_list: Optional[list] = None
        self.target_users: Optional[list] = None
        self.reference_users: Optional[list] = None

    def populate_groups(self):
        """
        Use object properties to get a comparable list of workbooks from the source and reference
        """

        full_target_groups, full_target_groups_list = self.generate_server_list(
            self.plan.target, self.AssetType.Groups
        )

        self.target_groups_list = list(
            filter(lambda x: x != "All Users", full_target_groups_list)
        )

        self.target_groups = list(
            filter(lambda x: x.name != "All Users", full_target_groups)
        )

        group_memberships = list()

        for group in self.target_groups:
            with self.plan.target.connect():
                self.plan.target.server.groups.populate_users(group)

                group_membership_dict = {"group_name": group.name, "users": []}

                for user in group.users:
                    group_membership_dict.get("users").append(user.name)

                group_memberships.append(group_membership_dict)

        self.target_group_memberships_list = group_memberships

        # Load the spec as part of the Plan?
        """plan_reference = self.plan.raw_plan.get("reference")
        spec_file_path = plan_reference.get("file_path")

        raw_spec = YamlConnector(spec_file_path)

        spec = Specification()
        spec.load_spec(raw_spec.get_yaml())"""

        spec = self.plan.reference

        filtered_groups = list(
            filter(lambda x: x.get("group_name") != "All Users", spec.groups)
        )

        self.reference_groups_list = list(x.get("group_name") for x in filtered_groups)

        self.reference_group_memberships_list = filtered_groups.copy()

        for group in self.reference_group_memberships_list:
            group.update({"users": []})
            for user in spec.users:
                if user.get("user_name_domain"):
                    full_user_name = (
                        user.get("user_name") + "@" + user.get("user_name_domain")
                    )
                else:
                    full_user_name = user.get("user_name")
                if "groups" in user:
                    for user_group in user.get("groups"):
                        if user_group == group.get("group_name"):
                            group.get("users").append(full_user_name)

                        if user_group not in (
                            x.get("group_name")
                            for x in self.reference_group_memberships_list
                        ):
                            logger.warning(
                                f"An exception occurred: Group {user_group} on user {full_user_name} is not valid"
                            )

    def populate_users(self):
        full_target_users, full_target_users_list = self.generate_server_list(
            self.plan.target, self.AssetType.Users
        )

        self.target_users = full_target_users

    def _generate_server_list(
        self, source, asset_type, request_filter: Optional[TSC.RequestOptions] = None
    ):
        """

        :param source:
        :param asset_type:
        :param filter:
        :return:
        """
        asset = getattr(source.server, asset_type)

        with source.connect():
            asset_items = list(TSC.Pager(asset, request_filter))
            """
              Generalized: can be moved to parent class
              Find a way to included updated_at check.  Might be able to use dict to
              """

            asset_list = []
            for asset in asset_items:
                asset_list.append(asset.name)
            return asset_items, asset_list

    def get_group_changes(self):
        """

        :return:
        """
        common, to_remove, to_add = self.get_changes(
            self.target_groups_list, self.reference_groups_list
        )

        update_list = list()

        for group_name in common:
            reference_membership, target_membership = self.get_group_memberships(
                group_name
            )

            logger.debug(
                f"Group: {group_name} | Target: {set(target_membership)} | Reference: {set(reference_membership)} | Check: {set(target_membership) != set(reference_membership)}"
            )

            if set(target_membership) != set(reference_membership):
                update_list.append(group_name)

        return to_add, to_remove, update_list

    def get_group_memberships(self, group_name):
        reference_membership_group = utils.get_filtered_dict_list(
            self.reference_group_memberships_list, group_name, "group_name"
        )[0]
        reference_membership = reference_membership_group.get("users")

        try:
            target_membership_group = utils.get_filtered_dict_list(
                self.target_group_memberships_list, group_name, "group_name"
            )[0]

            target_membership = target_membership_group.get("users")
        except:
            target_membership = list()

        logger.debug(
            f"Group: {group_name} | Reference Memberships: {self.reference_group_memberships_list} | Target Memberships: {self.target_group_memberships_list} | Reference Users: {reference_membership} | Target Users: {target_membership} "
        )

        return reference_membership, target_membership

    def delete_group(self, group):
        with self.plan.target.connect():
            self.plan.target.server.groups.delete(group.id)
            logger.info(f"Group {group.name} was removed from the server")

    def create(self, group_name):
        # create a new instance with the group name
        new_group = TSC.GroupItem(group_name)

        with self.plan.target.connect():
            created_group = self.plan.target.server.groups.create(new_group)
            logger.info(f"Group {created_group} was added to the server")

        return created_group

    def add_user(self, group_item, user_item):
        with self.plan.target.connect():
            self.plan.target.server.groups.add_user(group_item, user_item.id)
        logger.info(f"User {user_item.name} was added to group {group_item.name}")

    def remove_user(self, group_item, user_item):
        with self.plan.target.connect():
            self.plan.target.server.groups.remove_user(group_item, user_item.id)
        logger.info(f"User {user_item.name} was removed from group {group_item.name}")

    def update_group_membership(self, group_item):
        group_name = group_item.name
        reference_membership, target_membership = self.get_group_memberships(group_name)

        common, to_remove, to_add = self.get_changes(
            target_membership, reference_membership
        )

        logger.debug(f"Group: {group_name}, Add: {to_add}, Remove: {to_remove}")

        for user in to_add:
            user_item = utils.get_item_from_list(user, self.target_users)
            self.add_user(group_item, user_item)

        for user in to_remove:
            user_item = utils.get_item_from_list(user, self.target_users)
            self.remove_user(group_item, user_item)

        logger.info(f"Added {len(to_add)} users and removed {len(to_remove)} users")

    def add(self, list_to_add: list):
        """ """

        if len(list_to_add) > 0:
            for group_name in list_to_add:
                logger.info(f"Processing the addition of Group: {group_name}")

                created_group = self.create(group_name)

                self.update_group_membership(created_group)

        logger.info(f"Added {len(list_to_add)} Groups")

    def remove(self, remove_list: list):
        """
        Match the workbook from list to reference object
        Delete Workbook
        """
        if len(remove_list) > 0:
            for group_name in remove_list:
                group = self.get_item_from_list(group_name, self.target_groups)
                logger.debug(f"Group to Remove: {group}")

                self.delete_group(group)
        logger.info(f"Removed {len(remove_list)} Groups")

    def update(self, update_list: list):
        """ """
        if len(update_list) > 0:
            for group_name in update_list:
                group_item = self.get_item_from_list(group_name, self.target_groups)

                self.update_group_membership(group_item)
        logger.info(f"Updated {len(update_list)} Groups")
