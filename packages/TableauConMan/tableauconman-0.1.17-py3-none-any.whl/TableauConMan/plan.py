"""Module management of provided plans"""
import os

import tableauserverclient as TSC
from TableauConMan.server_connector import ServerConnector
from TableauConMan.yaml_connector import YamlConnector
from TableauConMan.specification import Specification
from loguru import logger


class Plan:
    """
    Plan class represents a plan for data manipulation in a system.

    Attributes:
        target (str): The target connection for the plan.
        reference (str): The reference connection for the plan.
        target_selection_rules (TSC.RequestOptions): The selection rules for the target connection.
        reference_selection_rules (TSC.RequestOptions): The selection rules for the reference connection.
        assets (list): The assets to be manipulated by the plan.
        asset_options (dict): The options for the assets.
        operation (str): The operation to be performed by the plan.
        connections (dict): The connections used by the plan.
        raw_plan (dict): The raw plan data.

    Note:
        - The `target` and `reference` attributes represent connection objects.
        - The selection rules are instances of the `TSC.RequestOptions` class.
        - The assets are represented by a list.
        - The asset options are represented by a dictionary.
        - The operation is represented by a string.
        - The connections are represented by a dictionary.
        - The raw plan is represented by a dictionary.
    """

    def __init__(self):
        self.target: str = None
        self.reference: str = None
        self.target_selection_rules: TSC.RequestOptions() = None
        self.reference_selection_rules: TSC.RequestOptions() = None
        self.assets: list = None
        self.asset_options: dict = None
        self.operation: str = None
        self.connections: dict = None
        self.raw_plan: dict = None
        self.default_workbook_owner: str = None
        self.deleted_user_archive_project: str = None

    def load_plan(self, raw_plan: dict) -> None:
        """

        :param raw_plan:
        """
        if not isinstance(raw_plan, dict):
            raise TypeError("The raw plan must be a dictionary")

        self.target = self.format_connection(raw_plan.get("target"))
        self.reference = self.format_connection(raw_plan.get("reference"))
        self.target_selection_rules = self.format_rule(
            raw_plan.get("target_selection_rules")
        )
        self.reference_selection_rules = self.format_rule(
            raw_plan.get("reference_selection_rules")
        )
        self.assets = list(raw_plan.get("assets"))
        self.asset_options = raw_plan.get("assets")
        self.operation = raw_plan.get("operation")
        self.connections = raw_plan.get("connections")
        self.default_workbook_owner = os.environ.get(
            raw_plan.get("target").get("default_workbook_owner")
        )
        self.deleted_user_archive_project = os.environ.get(
            raw_plan.get("target").get("deleted_user_archive_project")
        )
        self.raw_plan = raw_plan

    @staticmethod
    def format_rule(rules):
        """

        :param rules:
        :return:
        """
        formatted_rule = TSC.RequestOptions()

        if rules:
            for rule in rules:
                field = getattr(formatted_rule.Field, rule.get("field"))
                operator = getattr(formatted_rule.Operator, rule.get("operator"))
                value = rule.get("value")
                formatted_rule.filter.add(TSC.Filter(field, operator, value))

        return formatted_rule

    def format_connection(self, connection):
        """

        :param connection:
        :return:
        """
        connection_type = connection.get("type")

        if connection_type == "server":
            connection = self.format_server(connection)
        elif connection_type == "spec":
            connection = self.format_spec(connection)

        return connection

    def format_server(self, connection):
        """

        :param connection:
        :return:
        """
        (
            token_name,
            token_secret,
            server_url,
            site_name,
        ) = self.get_server_secrets_from_env(connection)

        server = ServerConnector(site_name, server_url, token_name, token_secret)

        return server

    def format_spec(self, connection):
        """

        :param connection:
        :return:
        """
        spec_file_path = connection.get("file_path")

        raw_spec = YamlConnector(spec_file_path)

        spec = Specification()
        spec.load_spec(raw_spec.get_yaml())

        return spec

    @staticmethod
    def get_server_secrets(server):
        """

        :param server:
        :return:
        """
        token_name = server.get("token_name")
        token_secret = server.get("token_secret")
        server_url = server.get("server_url")
        site_name = server.get("site_name")

        return token_name, token_secret, server_url, site_name

    def get_server_secrets_from_env(self, server):
        """

        :param server:
        :return:
        """
        token_name = os.environ.get(server.get("token_name")).strip()
        token_secret = os.environ.get(server.get("token_secret")).strip()
        server_url = os.environ.get(server.get("server_url")).strip()
        site_name = os.environ.get(server.get("site_name")).strip()

        return token_name, token_secret, server_url, site_name

    @staticmethod
    def get_connection_secretes(connection):
        """

        :param connection:
        :return:
        """

        username = os.environ.get(connection.get("username")).strip()
        password = os.environ.get(connection.get("password")).strip()

        return username, password
