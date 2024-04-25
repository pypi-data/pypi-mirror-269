from TableauConMan.sources.sources import Source
from TableauConMan.assets.asset import Asset
from TableauConMan.managers.asset_manager import AssetManager
from TableauConMan.managers.permission_rule_manager import PermissionRuleManager
from TableauConMan.factories.converter_factory import ConverterFactory
import TableauConMan.config.plan_options as options

from typing import List, Tuple
from loguru import logger


class ProjectManager(AssetManager):
    def __init__(self) -> None:
        super().__init__(),
        self.permission_rule_manager = PermissionRuleManager()
        self.converter_factory = ConverterFactory()

    def add(
        self, asset_type: str, project_asset_list: List[Asset], target_source: Source
    ):
        """ """
        asset_converter = self.converter_factory.get_asset_converter(
            asset_type, target_source
        )

        for project_asset in project_asset_list:
            converted_project = asset_converter.convert_to_source(project_asset)
            created_project = target_source.add_item(asset_type, converted_project)

            logger.info(f"Project {created_project} added.")

            self.permission_rule_manager.add(
                target_source, created_project, project_asset
            )

    def remove(
        self, asset_type: str, project_item_list: List[Asset], target_source: Source
    ):
        if options.DELETE_ON_TARGET:
            project_item_list = self.get_source_list(
                asset_type, project_item_list, target_source
            )
            for project in project_item_list:
                target_source.delete_item(asset_type, project)

                logger.debug(f"Deleted project: {project}")

    def update(
        self,
        asset_type: str,
        project_item_list: List[Tuple[Asset, Asset]],
        target_source: Source,
    ):
        # logger.debug(f"Assets to Update: {project_item_list}")

        asset_converter = self.converter_factory.get_asset_converter(
            asset_type, target_source
        )

        for target_item, reference_item in project_item_list:
            target_item.update_asset(reference_item)

            converted_project = asset_converter.convert_to_source(target_item)

            updated_project = target_source.update_item(asset_type, converted_project)

            self.permission_rule_manager.update(
                target_source, updated_project, target_item, reference_item
            )

            logger.debug(f"Updated project: {updated_project}")
