from TableauConMan.converters.converter import Converter
from TableauConMan.converters.project_converter import ProjectConverter
from TableauConMan.converters.permission_rule_converter import PermissionRuleConverter
from TableauConMan.sources.sources import Source
from loguru import logger


class ConverterFactory:
    @staticmethod
    def get_asset_converter(asset_type: str, asset_source: Source) -> Converter:
        if asset_type == "projects":
            asset_converter = ProjectConverter(asset_source)
        elif asset_type == "permission_rule":
            asset_converter = PermissionRuleConverter(asset_source)
        else:
            raise TypeError(f"No converter for the {asset_type} asset_type")

        return asset_converter
