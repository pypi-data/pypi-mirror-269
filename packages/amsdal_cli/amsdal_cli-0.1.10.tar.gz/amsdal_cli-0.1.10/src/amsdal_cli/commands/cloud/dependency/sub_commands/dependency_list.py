import json
from pathlib import Path
from typing import Annotated

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table
from typer import Option

from amsdal_cli.commands.cloud.dependency.app import dependency_sub_app
from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.utils.cli_config import CliConfig


@dependency_sub_app.command(name='list')
def dependency_list_command(
    ctx: typer.Context,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
    *,
    sync: bool = Option(
        False,
        '--sync',
        help='Sync the dependencies from the Cloud Server to ".dependencies".',
    ),
) -> None:
    """
    List the app dependencies on the Cloud Server.
    """
    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        list_response = manager.cloud_actions_manager.list_dependencies(
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        raise typer.Exit(1) from e

    if sync:
        _deps_path: Path = cli_config.app_directory / '.dependencies'
        _deps_path.touch(exist_ok=True)
        _deps_path.write_text('\n'.join(list_response.dependencies))

    if not list_response:
        return

    if output == OutputFormat.json:
        print(json.dumps(list_response.model_dump(), indent=4))
        return

    if not list_response.dependencies:
        print('No dependencies found.')
        return

    data_table = Table()
    data_table.add_column('Dependency Name', justify='center')

    for dependency in list_response.dependencies:
        data_table.add_row(dependency)

    print(data_table)
