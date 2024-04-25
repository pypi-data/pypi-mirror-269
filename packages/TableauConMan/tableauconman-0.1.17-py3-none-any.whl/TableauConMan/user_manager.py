from typing import Optional, Dict, List
from TableauConMan.assets_manager import AssetsManager
from TableauConMan.helpers import utils
import tableauserverclient as TSC
from loguru import logger
import time
import requests


class UserManager(AssetsManager):
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

    def populate_server_users(self) -> Dict:
        """

        :return:
        """
        logger.info("Retrieving server users")
        with self.plan.target.connect():
            clean_dict = {
                user.email: user.site_role
                for user in TSC.Pager(self.plan.target.server.users)
            }
        logger.success("Server users retrieved")
        return clean_dict

    def create_user(self, user_name: str, role: str):
        """

        :param user_name:
        :param role:
        :return:
        """
        logger.info(f"Creating user: {user_name}, role: {role}")
        new_user = TSC.UserItem(user_name, role, auth_setting="SAML")

        with self.plan.target.connect():
            new_u = self.plan.target.server.users.add(new_user)
            logger.success("User added successfully")
            return new_u.id

    def delete_user_rest_api(self, user_to_delete_id: str, admin_user_id: str):
        """

        :param user_to_delete_id:
        :param admin_user_id:
        :return:
        """
        with self.plan.target.connect():
            headers = {
                "X-Tableau-Auth": self.plan.target.server.auth_token,
                "Content-Type": "application/json",
            }
            params = {"mapAssetsTo": admin_user_id}
            api_url = f"{self.plan.target.server_url}api/3.22/sites/{self.plan.target.server.site_id}/users/{user_to_delete_id}"

            response = requests.delete(api_url, headers=headers, params=params)

            if response.status_code == 204:
                logger.success("User deleted successfully")
                logger.success(response)
            else:
                logger.error(f"Error: {response.text}")

    def delete_user(
        self, user_name: str, admin_user: str, user_archive_folder: str
    ) -> bool:
        """

        :param user_name:
        :param admin_user:
        :param user_archive_folder:
        :return:
        """
        logger.info(f"Deleting {user_name}")
        user_to_delete = self.get_user_by_name(user_name)
        admin_user = self.get_user_by_name(admin_user)

        with self.plan.target.connect():
            server_projects = {
                proj.id: proj.name
                for proj in TSC.Pager(self.plan.target.server.projects)
            }
            archive_project_id = next(
                (
                    id
                    for id, name in server_projects.items()
                    if name == user_archive_folder
                ),
                None,
            )

            if archive_project_id is None:
                logger.error(
                    f"Please ensure the archive folder {user_archive_folder} has been created"
                )
                exit(1)

        with self.plan.target.connect():
            # Req options filtering doesn't work well for this endpoint, we need to filter it manually.
            workbooks = [
                workbook
                for workbook in user_to_delete.workbooks
                if workbook.owner_id == user_to_delete.id
            ]

            if len(workbooks) > 0:
                logger.info(
                    f"User {user_name} owns {len(workbooks)} workbooks, updating these to {admin_user}"
                )
                admin_user = self.get_user_by_name(admin_user)

            with self.plan.target.connect():
                for w in workbooks:
                    w.owner_id = admin_user.id

                    if (
                        w.project_name is None
                        and server_projects.get(w.project_id) is None
                    ):
                        logger.info(
                            f"Workbook {w.name} exists in {user_name} personal space, moving it to {user_archive_folder}"
                        )

                        w.project_id = archive_project_id

                        logger.info(
                            f"Updating {w.name} to {w.name}_{user_name}_{time.strftime('%Y%m%d-%H%M%S')}"
                        )

                        w.name = (
                            f"{w.name}_{user_name}_{time.strftime('%Y%m%d-%H%M%S')}"
                        )

                    self.plan.target.server.workbooks.update(w)
                    logger.success(f"{w.name} updated")

        self.delete_user_rest_api(user_to_delete.id, admin_user.id)

        return True

    def update_user_roles(self, user_name: str, role: str) -> bool:
        """

        :param user_name:
        :param role:
        :return:
        """
        logger.info(f"Updating user: {user_name}")
        update_user = self.get_user_by_name(user_name)

        update_user.site_role = role

        with self.plan.target.connect():
            self.plan.target.server.users.update(update_user)

        logger.success("User updated")
        return True

    def get_user_by_name(self, user_name: str) -> TSC.UserItem:
        """

        :param user_name:
        :return:
        """
        # Sets up the request param to filter for the correct username.
        req_option = TSC.RequestOptions()
        req_option.filter.add(
            TSC.Filter(
                TSC.RequestOptions.Field.Name,
                TSC.RequestOptions.Operator.Equals,
                user_name,
            )
        )
        with self.plan.target.connect():
            all_users, pagination_item = self.plan.target.server.users.get(
                req_options=req_option
            )

            if pagination_item.total_available > 1:
                raise ValueError(
                    f"Multiple user names have been returned, {pagination_item.total_available}."
                )

            if pagination_item.total_available < 1:
                logger.warning(
                    f"No user was found matching the user name {user_name} on the site."
                )
                return

            self.plan.target.server.users.populate_workbooks(all_users[0])

            return all_users[0]

    def compare_dicts(self, reference: Dict, target: Dict) -> [List, List, Dict]:
        """

        :param reference:
        :param target:
        :return:
        """
        keys_only_in_reference = [key for key in reference if key not in target]
        keys_only_in_target = [key for key in target if key not in reference]
        keys_with_different_values = [
            (key, reference[key])
            for key in reference
            if key in target and reference[key] != target[key]
        ]

        return keys_only_in_reference, keys_only_in_target, keys_with_different_values
