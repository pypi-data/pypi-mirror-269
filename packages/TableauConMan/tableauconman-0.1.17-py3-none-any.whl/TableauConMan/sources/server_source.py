import os
from typing import Any, List, Optional, Type
from dataclasses import dataclass

import tableauserverclient as TSC
from loguru import logger


@dataclass
class ServerSource:
    """Class representing the connection details and methods for connecting to a Tableau server"""

    def __init__(
        self,
        site_name: Optional[str] = None,
        server_url: Optional[str] = None,
        token_name: Optional[str] = None,
        token_secret: Optional[str] = None,
    ):
        self.site_name: Optional[str] = site_name
        self.server_url: Optional[str] = server_url
        self.token_name: Optional[str] = token_name
        self.token_secret: Optional[str] = token_secret
        self.authentication: Optional[TSC.PersonalAccessTokenAuth] = None
        self.server: Optional[TSC.Server] = None
        self.source_type: str = "server"

    """def __repr__(self):

        return "<Server {site_name} server_object={_server} auth_object={_authentication}>".format(
            **self.__dict__
        )"""

    @property
    def name(self) -> str:
        return self.site_name

    @property
    def server(self) -> Optional[TSC.Server]:
        """

        :return:
        """
        return self._server

    @server.setter
    def server(self, value):
        if value is None:
            self._server = TSC.Server(self.server_url, use_server_version=True)
        elif not isinstance(value, TSC.Server):
            raise TypeError("server must be of TSC.Server class")
        else:
            self._server = value

    @property
    def authentication(self) -> TSC.PersonalAccessTokenAuth:
        """

        :return:
        """
        return self._authentication

    @authentication.setter
    def authentication(self, value):
        if value is None:
            self._authentication = TSC.PersonalAccessTokenAuth(
                self.token_name,
                self.token_secret,
                site_id=self.site_name,
            )
        elif not isinstance(value, TSC.PersonalAccessTokenAuth):
            raise TypeError(
                "authentication must be of  TSC.PersonalAccessTokenAuth class"
            )
        else:
            self._authentication = value

    def connect(self):
        """

        :return:
        """
        connection = self.server.auth.sign_in(self.authentication)

        return connection

    def get_assets(
        self,
        asset_type: str,
        request_filter: Optional[TSC.RequestOptions] = None,
    ) -> List[Any]:
        """

        :param source:
        :param asset_type:
        :param filter:
        :return:
        """
        asset = getattr(self.server, asset_type)

        with self.connect():
            asset_items = list(TSC.Pager(asset, request_filter))
            return asset_items

    def delete_item(self, asset_type: str, item_to_delete):
        server_item = getattr(self.server, asset_type)

        with self.connect():
            server_item.delete(item_to_delete.id)

    def add_item(self, asset_type: str, item_to_delete):
        server_item = getattr(self.server, asset_type)

        with self.connect():
            new_item = server_item.create(item_to_delete)

        return new_item

    def update_item(self, asset_type: str, item_to_delete):
        server_item = getattr(self.server, asset_type)

        with self.connect():
            updated_item = server_item.update(item_to_delete)

        return updated_item

    def add_sub_item(self, asset_type: str, target_item, sub_item) -> None:
        target_item = self.populate_default_permissions(target_item, asset_type)
        with self.connect():
            server_add_function = self._get_project_permission_method(
                asset_type, "update"
            )
            # TSC is expecting a list of rules.
            server_add_function(target_item, [sub_item])

    def remove_sub_item(self, asset_type: str, target_item, sub_item) -> None:
        target_item = self.populate_default_permissions(target_item, asset_type)
        with self.connect():
            server_add_function = self._get_project_permission_method(
                asset_type, "delete"
            )
            server_add_function(target_item, sub_item)

    def update_sub_item(self):
        ...

    def populate_default_permissions(
        self, project_item: TSC.ProjectItem, asset_type: str
    ) -> TSC.ProjectItem:
        populate_method = self._get_project_permission_method(asset_type, "populate")

        with self.connect():
            populate_method(project_item)
            return project_item

    def _get_project_permission_method(self, asset_type, action):
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

        permission_method = getattr(self.server.projects, permission_method_name)

        return permission_method

    def _get_project_permission_object(self, asset_type, project_item):
        if asset_type == "project":
            permission_object_name = "permissions"
        else:
            permission_object_name = f"default_{asset_type}_permissions"

        permission_object = getattr(project_item, permission_object_name)

        return permission_object

    @classmethod
    def load(cls: Type["ServerSource"], source_config: dict):
        return cls(
            token_name=os.environ.get(source_config.get("token_name")).strip(),
            token_secret=os.environ.get(source_config.get("token_secret")).strip(),
            server_url=os.environ.get(source_config.get("server_url")).strip(),
            site_name=os.environ.get(source_config.get("site_name")).strip(),
        )
