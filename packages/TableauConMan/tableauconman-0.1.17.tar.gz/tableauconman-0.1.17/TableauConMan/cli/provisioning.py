from TableauConMan.plan import Plan
from TableauConMan.workbooks_manager import WorkbooksManager
from TableauConMan.data_sources_manager import DataSourcesManager
from TableauConMan.projects_manager import ProjectsManager
from TableauConMan.groups_manager import GroupsManager
from TableauConMan.user_manager import UserManager
from TableauConMan.yaml_connector import YamlConnector

from TableauConMan.config.plans import Plan as plan_v2
from TableauConMan.factories.manager_factory import AssetManagerFactory
import TableauConMan.config.plan_options as options

from loguru import logger
from dotenv import load_dotenv
from . import cli
import click

load_dotenv()


@cli.command("provision-projects", help="Provision projects")  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def provision_projects(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)
    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")
    provision_projects(plan)


@cli.command("provision-users", help="Provision users")  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def provision_users(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)
    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")
    process_user_provisioning(plan)


# "./public_sync_plan.yaml"
@cli.command("migrate-content", help="Migrate content from one site to another.")  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def migrate_content(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info("Loaded plan")

    migrate_datasources(plan)

    migrate_workbooks(plan)


@cli.command("provision-settings", help="Provision settings")  # type: ignore
@click.option(
    "--yaml_path",
    help="String path of where the yaml plan is located",
)
def provision_settings(yaml_path: str):
    """

    :param yaml_path:
    :return:
    """
    raw_plan = YamlConnector(yaml_path)

    plan = Plan()
    plan.load_plan(raw_plan.get_yaml())
    logger.info(raw_plan.get_yaml())
    logger.info("Loaded plan")

    provision_groups(plan)


@cli.command()
@click.option(
    "--plan-file",
    "-p",
    type=click.Path(),
    help="String path of where the yaml plan is located",
)
def configure_assets(plan_file: str):
    """_summary_

    :param plan_file: _description_
    """
    raw_plan = YamlConnector(plan_file)

    file_text_list = raw_plan.get_yaml()

    # Load

    plan = plan_v2().load(file_text_list)
    logger.info("Loaded plan")

    load_project_options(plan.project_options)

    configure_projects(plan)


def migrate_datasources(migrate_plan: Plan):
    datasources = DataSourcesManager(migrate_plan)
    logger.info("Processing Datasources")
    datasources.populate_datasources()
    logger.info("Populated datasources")
    # logger.debug(datasources.reference_datasources)

    datasource_options = datasources.get_datasource_options()

    to_update, to_add, to_remove = datasources.get_datasource_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    datasources.remove(to_remove)

    datasources.add(
        to_add,
        to_update,
        datasource_options,
    )

    logger.info("Processed Datasources")


def migrate_workbooks(migration_plan: Plan):
    logger.info("Processing Workbooks")
    workbooks = WorkbooksManager(migration_plan)
    workbooks.populate_workbooks()
    logger.info("Populated workbooks")
    logger.debug(workbooks.reference_workbooks)

    workbook_options = workbooks.get_workbook_options()
    to_update, to_add, to_remove = workbooks.get_workbook_changes()
    logger.debug(f"Update:{to_update}, Add:{to_add}, Remove:{to_remove}")

    workbooks.remove(to_remove)

    workbooks.add(to_add, to_update, workbook_options)

    logger.info("Processed Workbooks")


def process_project_provisioning(provision_plan: Plan):
    logger.info("Processing Projects")
    projects = ProjectsManager(provision_plan)
    projects.populate_projects()
    logger.info("Populated projects")
    logger.debug(f"Reference Projects: {projects.reference_projects}")
    logger.debug(f"Reference Project List: {projects.reference_projects_list}")
    logger.debug(f"Target Projects: {projects.target_projects}")
    logger.debug(f"Target Project List: {projects.target_projects_list}")
    logger.debug(f"Target Project Path List: {projects.target_project_paths_list}")
    logger.debug(
        f"Reference Project Path List: {projects.reference_project_paths_list}"
    )

    to_update, to_remove, to_add = projects.get_project_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    projects.add(to_add)

    projects.remove(to_remove)

    projects.update(to_update)

    logger.info("Processed Projects")

    project_options = projects.get_project_options()

    if project_options.get("update_permissions"):
        logger.info("Processing Permissions")
        projects.populate_projects()
        logger.info("Populated projects")
        projects.populate_users_and_groups()
        projects.populate_project_permissions()
        projects.populate_permission_capabilities()

        """logger.debug(
            f"Target Capabilities: {projects.target_project_capabilities_list}"
        )"""
        """logger.debug(
            f"Reference Capabilities: {projects.reference_project_capabilities_list}"
        )"""

        to_update, to_remove, to_add = projects.get_permission_changes()
        # logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")
        logger.debug(f"Add:{to_add}")
        logger.debug(f"Remove:{to_remove}")
        # logger.debug(f"Update: {to_update}")

        projects.add_capabilities(to_add)

        projects.remove_capabilities(to_remove)

    logger.info("Processed Permissions")


def configure_projects(configure_plan: plan_v2):
    for asset_type in options.ConfigureAssets:
        if asset_type.value in configure_plan.assets:
            asset_manager = AssetManagerFactory.get_asset_manager(asset_type.value)

            target_asset_list = asset_manager.get_asset_list(
                asset_type.value, configure_plan.target
            )

            reference_asset_list = asset_manager.get_asset_list(
                asset_type.value, configure_plan.reference
            )

            logger.info(f"Loaded Target and Reference for {asset_type}.")

            (
                assets_to_add,
                assets_to_remove,
                assets_to_update,
            ) = asset_manager.group_asset_list(target_asset_list, reference_asset_list)

            asset_manager.add(asset_type.value, assets_to_add, configure_plan.target)

            asset_manager.remove(
                asset_type.value, assets_to_remove, configure_plan.target
            )

            asset_manager.update(
                asset_type.value, assets_to_update, configure_plan.target
            )

        logger.info(f"Completed processing of {asset_type.value}")


def provision_groups(provision_plan: Plan):
    logger.info("Processing Groups")
    groups = GroupsManager(provision_plan)
    groups.populate_groups()
    logger.info("Populated groups")
    logger.debug(f"Target Groups: {groups.target_groups_list}")
    logger.debug(f"Reference Groups: {groups.reference_groups_list}")
    logger.debug(f"Target Group Memberships: {groups.target_group_memberships_list}")
    logger.debug(
        f"Reference Group Memberships: {groups.reference_group_memberships_list}"
    )
    groups.populate_users()

    to_add, to_remove, to_update = groups.get_group_changes()
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    groups.remove(to_remove)

    groups.add(to_add)

    groups.update(to_update)

    logger.info("Processed Groups")


def process_user_provisioning(provision_plan: Plan):
    """

    :param provision_plan:
    :return:
    """

    user_manager = UserManager(provision_plan)

    if provision_plan.default_workbook_owner is None:
        logger.error(
            "Please set the default_workbook_owner key in provisioning plan.yaml, "
            "addressing an environment variable before proceeding."
        )
        exit(1)

    if provision_plan.deleted_user_archive_project is None:
        logger.error(
            "Please set the deleted_user_archive_project key in provisioning plan.yaml, "
            "addressing an environment variable before proceeding."
        )
        exit(1)

    server_user_dict = user_manager.populate_server_users()

    reference_users = provision_plan.reference.users
    reference_user_dict = {
        f"{r.get('user_name')}@{r.get('user_name_domain')}": r.get("site_role")
        for r in reference_users
    }
    to_add, to_remove, to_update = user_manager.compare_dicts(
        reference_user_dict, server_user_dict
    )
    logger.debug(f"Add:{to_add}, Remove:{to_remove}, Update: {to_update}")

    [user_manager.create_user(a, reference_user_dict.get(a)) for a in to_add]
    [user_manager.update_user_roles(a[0], a[1]) for a in to_update]
    [
        user_manager.delete_user(
            a,
            provision_plan.default_workbook_owner,
            provision_plan.deleted_user_archive_project,
        )
        for a in to_remove
    ]
    logger.info("Processed users")


def load_project_options(project_options: dict) -> None:
    options.INCLUDE_ASSET_PERMISSIONS = project_options.get("include_asset_permissions")
