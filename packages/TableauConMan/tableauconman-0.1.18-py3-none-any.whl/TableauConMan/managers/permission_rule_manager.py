from TableauConMan.sources.sources import Source
from TableauConMan.assets.permission_rule_asset import PermissionRule
from TableauConMan.managers.asset_manager import AssetManager
from TableauConMan.factories.converter_factory import ConverterFactory


from loguru import logger


class PermissionRuleManager(AssetManager):
    def __init__(self) -> None:
        super().__init__()
        self.converter_factory = ConverterFactory()

    def add(
        self, target_source: Source, target_project_item, reference_project_asset
    ) -> None:
        asset_converter = self.converter_factory.get_asset_converter(
            "permission_rule", target_source
        )
        logger.debug(reference_project_asset)
        for permission_rule in reference_project_asset.permission_set:
            asset_type = permission_rule.asset_type

            converted_permission_rule = asset_converter.convert_to_source(
                permission_rule
            )

            target_source.add_sub_item(
                asset_type, target_project_item, converted_permission_rule
            )

            logger.info(f"Added {asset_type} Permissions for {target_project_item}.")

    def remove(self):
        logger.info(f"Removed Permissions")

    def update(
        self,
        target_source: Source,
        target_project_item,
        target_project_asset,
        reference_project_asset,
    ) -> None:
        asset_converter = self.converter_factory.get_asset_converter(
            "permission_rule", target_source
        )

        add, remove, update = self.get_update_lists(
            target_project_asset, reference_project_asset
        )

        for target_rule, reference_rule in update:
            in_a_and_b = sorted(
                list(
                    set(target_rule.capabilities.items())
                    & set(reference_rule.capabilities.items())
                )
            )
            in_a_not_b = sorted(
                list(set(target_rule.capabilities.items()) ^ set(in_a_and_b))
            )
            in_b_not_a = sorted(
                list(set(reference_rule.capabilities.items()) ^ set(in_a_and_b))
            )

            if len(in_a_not_b) > 0:
                remove_rule = PermissionRule(
                    asset_type=target_rule.asset_type,
                    grantee_name=target_rule.grantee_name,
                    grantee_type=target_rule.grantee_type,
                    capabilities=dict(),
                )

                for capability, mode in in_a_not_b:
                    remove_rule.capabilities.update({capability: mode})

                remove.append(remove_rule)

            if len(in_b_not_a) > 0:
                add_rule = PermissionRule(
                    asset_type=target_rule.asset_type,
                    grantee_name=target_rule.grantee_name,
                    grantee_type=target_rule.grantee_type,
                    capabilities=dict(),
                )

                for capability, mode in in_b_not_a:
                    add_rule.capabilities.update({capability: mode})

                add.append(add_rule)

        combined_update = add

        for permission_rule in combined_update:
            asset_type = permission_rule.asset_type
            converted_permission_rule = asset_converter.convert_to_source(
                permission_rule
            )
            logger.debug(converted_permission_rule)
            target_source.add_sub_item(
                asset_type, target_project_item, converted_permission_rule
            )

            logger.info(
                f"Updated {asset_type} permissions for {permission_rule.grantee_name} on {target_project_asset.project_name}."
            )

        for permission_rule in remove:
            asset_type = permission_rule.asset_type
            converted_permission_rule = asset_converter.convert_to_source(
                permission_rule
            )

            target_source.remove_sub_item(
                asset_type, target_project_item, converted_permission_rule
            )
            logger.info(
                f"Removed {asset_type} permissions for {permission_rule.grantee_name} on {target_project_asset.project_name}."
            )
        logger.info(f"Updated Permissions")

    def get_update_lists(self, target_project_item, reference_project_item):
        add, remove, update = self.group_asset_list(
            target_project_item.permission_set, reference_project_item.permission_set
        )
        """logger.info(
            f"Updated Permissions: Add: {add} Remove: {remove} Update: {update}"
        )"""

        return add, remove, update
