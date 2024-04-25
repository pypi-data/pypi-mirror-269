from typing import Any, List, Type
import os

from dataclasses import dataclass
import yaml
import hashlib
import json
from TableauConMan.helpers import utils

from loguru import logger


class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


@dataclass
class SpecificationSource:
    """Class representing a connection to a yaml file or yaml string"""

    file_path: str = None
    source_type: str = "specification"

    @property
    def name(self) -> str:
        return self.file_path

    @property
    def file_text_list(self):
        return self.read_yaml()

    def read_yaml(self):
        """

        :param object:
        :return:
        """

        file_path_parts = os.path.split(self.file_path)
        search_path = file_path_parts[0]
        file_name = file_path_parts[1]
        # logger.debug(f"{os.getcwd()} | {search_path}: {file_name}")
        jinja_environment = utils.get_jinja_environment(search_path)

        try:
            file_text_list = yaml.safe_load(
                jinja_environment.get_template(file_name).render()
            )
            return file_text_list
        except yaml.YAMLError as exc:
            print(exc)
            return None

    def write_yaml(self, dict_file, filename):
        with open(f"{filename}", "w") as file:
            documents = yaml.dump(
                dict_file,
                file,
                default_flow_style=False,
                sort_keys=False,
                Dumper=IndentDumper,
            )

    def get_assets(self, asset_type: str) -> List[Any]:
        asset_list = self.file_text_list.get(asset_type)

        if asset_type == "projects":
            asset_list = self.read_permission_rules(asset_list)

        return asset_list

    def get_permission_template(self, project_permission: dict) -> dict:
        permission_templates = self.get_assets("permission_templates")
        # logger.debug(f"{permission_templates} | {project_permission}")
        template_name = project_permission.get("permission_rule")
        project_permission_rule = next(
            item for item in permission_templates if item.get("name") == template_name
        ).copy()

        project_permission_rule.pop("name")

        return project_permission_rule

    def read_permission_rules(self, project_specification_list: dict) -> List[dict]:
        for project_specification in project_specification_list:
            if project_specification.get("permission_set"):
                for permission in project_specification.get("permission_set"):
                    rule = self.get_permission_template(permission)

                    permission.update({"permission_rule": rule})

        return project_specification_list

    def write_permission_templates(
        self, file_text: dict, project_list: List[dict]
    ) -> dict:
        permission_templates_list = list()

        for project in project_list:
            for permission_rule in project.get("permission_set"):
                permission_template = permission_rule.copy()
                permission_template_id = hashlib.md5(
                    json.dumps(permission_template, sort_keys=True).encode("utf-8")
                ).hexdigest()

                permission_rule.update({"permission_rule": permission_template_id})

                permission_template.update({"name": permission_template_id})

                for asset, capabilities in permission_template.get(
                    "permission_rule"
                ).items():
                    permission_template.update({asset: capabilities})

                permission_template.pop("permission_rule")

                if permission_template.get("group_name"):
                    permission_template.pop("group_name")

                if permission_template.get("user_name"):
                    permission_template.pop("user_name")

                permission_templates_list.append(permission_template)

        unique_permission_templates = list(
            {v.get("name"): v for v in permission_templates_list}.values()
        )

        file_text.update({"permission_templates": unique_permission_templates})

        return file_text, project_list

    def set_asset(self, asset_type: str, asset_list: List[dict]) -> None:
        current_file = self.file_text_list

        if asset_type == "projects":
            current_file, asset_list = self.write_permission_templates(
                current_file, asset_list
            )

        current_file.update({asset_type: asset_list})

        self.write_yaml(current_file, self.file_path)

    @classmethod
    def load(cls: Type["SpecificationSource"], source_config: dict):
        return cls(file_path=source_config.get("file_path"))
