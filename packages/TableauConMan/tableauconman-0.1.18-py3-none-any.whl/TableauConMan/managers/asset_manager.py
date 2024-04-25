from abc import ABC, abstractmethod
from TableauConMan.sources.sources import Source
from TableauConMan.assets.asset import Asset
from TableauConMan.factories.converter_factory import ConverterFactory
import TableauConMan.helpers.utils as utils


from typing import List
from loguru import logger


class AssetManager(ABC):
    def get_asset_list(self, asset_type: str, asset_source: Source) -> List[Asset]:
        asset_list = list()

        item_list = asset_source.get_assets(asset_type)

        converter_generator = ConverterFactory()

        asset_converter = converter_generator.get_asset_converter(
            asset_type, asset_source
        )

        for item in item_list:
            asset_spec = asset_converter.convert_to_asset(item)
            asset_list.append(asset_spec)

        return asset_list

    def get_source_list(
        self, asset_type: str, asset_list: List[Asset], asset_source: Source
    ) -> List[Asset]:
        source_item_list = list()

        converter_generator = ConverterFactory()

        asset_converter = converter_generator.get_asset_converter(
            asset_type, asset_source
        )

        for asset in asset_list:
            source_item = asset_converter.convert_to_source(asset)
            source_item_list.append(source_item)

        return source_item_list

    def asset_specification_ids(self, asset_list: List[Asset]) -> List[str]:
        return [item.specification_id for item in asset_list]

    def group_asset_list(
        self, target_asset_list: List[Asset], reference_asset_list: List[Asset]
    ) -> (List[Asset], List[Asset], List[Asset]):
        reference_assets_ids = self.asset_specification_ids(reference_asset_list)
        target_assets_ids = self.asset_specification_ids(target_asset_list)

        in_both, in_target_not_reference, in_reference_not_target = utils.compare_lists(
            target_assets_ids, reference_assets_ids
        )

        asset_to_add = [
            item
            for item in reference_asset_list
            if item.specification_id in in_reference_not_target
        ]

        assets_to_remove = [
            item
            for item in target_asset_list
            if item.specification_id in in_target_not_reference
        ]

        in_both = [
            item for item in reference_asset_list if item.specification_id in in_both
        ]

        assets_to_update = self.check_for_update(
            in_both, target_asset_list, reference_asset_list
        )

        return asset_to_add, assets_to_remove, assets_to_update

    def check_for_update(
        self,
        asset_list: List[Asset],
        target_asset_list: List[Asset],
        reference_asset_list: List[Asset],
    ) -> List[Asset]:
        assets_to_update = list()

        for asset in asset_list:
            # logger.debug(f"Asset: {asset} | Asset List: {target_asset_list}")
            target_asset = next(
                item
                for item in target_asset_list
                if item.specification_id == asset.specification_id
            )

            reference_asset = next(
                item
                for item in reference_asset_list
                if item.specification_id == asset.specification_id
            )
            """logger.debug(
                f"Target asset: {target_asset} Reference asset: {reference_asset}"
            )"""
            if (
                target_asset.update_checksum != reference_asset.update_checksum
                or target_asset.update_value < reference_asset.update_value
            ):
                assets_to_update.append(tuple((target_asset, reference_asset)))

                # logger.debug(f"Added item for update: {assets_to_update}")

        return assets_to_update

    @abstractmethod
    def add(asset_type: str, asset_list: List[Asset], target_source: Source) -> None:
        pass

    @abstractmethod
    def remove(asset_type: str, asset_list: List[Asset], target_source: Source) -> None:
        pass

    @abstractmethod
    def update(asset_type: str, asset_list: List[Asset], target_source: Source) -> None:
        pass
