"""Module for general Tableau Asset Manager"""
from TableauConMan.helpers import utils
from typing import Optional
import tableauserverclient as TSC


class AssetsManager:
    """

    :class: AssetsManager

    This class provides functionality for managing assets in a server.

    :class:`AssetType` defines different types of assets that can be managed using the `AssetsManager` class.
    """

    class AssetType:
        """

        :class: AssetType

        This class defines different types of assets.

        :class:`AssetType` has the following attributes:

        - `Workbooks`: Represents the asset type for workbooks.
        - `Datasources`: Represents the asset type for datasources.
        - `Groups`: Represents the asset type for groups.
        - `Projects`: Represents the asset type for projects.
        - `Users`: Represents the asset type for users.
        - `Workbook`: Represents the asset type for a single workbook.
        - `Project`: Represents the asset type for a single project.
        - `Datasource`: Represents the asset type for a single datasource.

        These attributes can be accessed using the `.` notation, like `AssetType.Workbooks`, `AssetType.Datasources`, etc.

        Example usage:

        .. code-block:: python

            # Accessing asset types
            workbook_type = AssetType.Workbooks
            datasource_type = AssetType.Datasources
            group_type = AssetType.Groups
            project_type = AssetType.Projects
            user_type = AssetType.Users
            single_workbook_type = AssetType.Workbook
            single_project_type = AssetType.Project
            single_datasource_type = AssetType.Datasource

            print(workbook_type)  # "workbooks"
            print(datasource_type)  # "datasources"
            print(group_type)  # "groups"
            print(project_type)  # "projects"
            print(user_type)  # "users"
            print(single_workbook_type)  # "workbook"
            print(single_project_type)  # "project"
            print(single_datasource_type)  # "datasource"

        """

        Workbooks = "workbooks"
        Datasources = "datasources"
        Groups = "groups"
        Projects = "projects"
        Users = "users"
        Workbook = "workbook"
        Project = "project"
        Datasource = "datasource"

    def __init__(self, plan) -> None:
        self.plan = plan

    @staticmethod
    def get_changes(list_a: list, list_b: list):
        """
        Compares the target and reference lists to get the differences
        """
        in_a_and_b, in_a_not_b, in_b_not_a = utils.compare_lists(list_a, list_b)

        return in_a_and_b, in_a_not_b, in_b_not_a

    @staticmethod
    def get_item_from_list(item_name, item_list):
        """
        Filters a list of items based on the name of the item
        """
        item = utils.get_item_from_list(item_name, item_list)

        return item

    def generate_server_list(
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

    def update_connection_credentials(self, asset, asset_type):
        """
        Updates the connection credentials with a valid ses of credentials
        """
        # logger.info(f"Processing Datasource Connections for: {datasource_name} | {uploaded_datasource.has_extracts}")
        valid_connections = self.plan.connections
        target = self.plan.target
        server_asset = getattr(target.server, asset_type)
        with target.connect():
            server_asset.populate_connections(asset)

            for connection in asset.connections:
                for valid_connection in valid_connections:
                    if connection.connection_type == valid_connection.get(
                        "type"
                    ):  # In a workbook Published Datasource are of connection_type = sqlproxy
                        username, password = self.plan.get_connection_secretes(
                            valid_connection
                        )

                        connection.username = username
                        connection.password = password
                        connection.embed_password = True

                        server_asset.update_connection(asset, connection)
