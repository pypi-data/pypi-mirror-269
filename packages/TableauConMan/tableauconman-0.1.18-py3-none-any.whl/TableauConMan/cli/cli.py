import click
import TableauConMan
from loguru import logger


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.version_option(version=TableauConMan.__version__, prog_name="TableauConMan")
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
