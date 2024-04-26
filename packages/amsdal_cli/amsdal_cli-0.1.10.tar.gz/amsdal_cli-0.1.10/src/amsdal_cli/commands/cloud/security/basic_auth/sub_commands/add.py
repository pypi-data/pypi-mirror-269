import json
from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print
from rich.table import Table

from amsdal_cli.commands.cloud.enums import OutputFormat
from amsdal_cli.commands.cloud.security.basic_auth.app import basic_auth_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@basic_auth_sub_app.command(name='add')
def add_basic_auth_command(
    ctx: typer.Context,
    *,
    username: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(
            '--username',
            '-u',
            help='Username for the Basic Auth. If not provided, a random username will be generated.',
        ),
    ] = None,
    password: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(
            '--password',
            '-p',
            help='Password for the Basic Auth. If not provided, a random password will be generated.',
        ),
    ] = None,
    output: Annotated[OutputFormat, typer.Option('--output', '-o')] = OutputFormat.default,
) -> None:
    """
    Add Basic Auth to the application API.
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        response = manager.cloud_actions_manager.add_basic_auth(
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            username=username,
            password=password,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    if not response.details:
        return

    print(
        'Basic Auth credentials have been added to the application. '
        'Please wait a few minutes for the changes to take effect.\n'
    )

    if output == OutputFormat.json:
        print(json.dumps(response.details.model_dump(), indent=4))
        return

    data_table = Table()

    data_table.add_column('Username', justify='center')
    data_table.add_column('Password', justify='center')

    data_table.add_row(
        response.details.username,
        response.details.password,
    )

    print(data_table)
