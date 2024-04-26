from pathlib import Path
from typing import Annotated
from typing import Optional

import typer
from amsdal.errors import AmsdalCloudError
from amsdal.manager import AmsdalManager
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.cloud.security.allowlist.app import allowlist_sub_app
from amsdal_cli.utils.cli_config import CliConfig


@allowlist_sub_app.command(name='add')
def add_allowlist_ip_command(
    ctx: typer.Context,
    *,
    ip_address: Annotated[
        Optional[str],  # noqa: UP007
        typer.Option(
            '--ip-address',
            help='IP address, range or combination of both to add to the allowlist. Will add your IP if not provided.',
        ),
    ] = None,
) -> None:
    """
    Add your IP to the allowlist of the API.

    ```shell
    Examples:

    > amsdal cloud security allowlist add
    > amsdal cloud security allowlist add --ip-address 0.0.0.0
    > amsdal cloud security allowlist add --ip-address 0.0.0.0/24
    > amsdal cloud security allowlist add --ip-address 0.0.0.0,1.0.0.0/24
    ```
    """

    cli_config: CliConfig = ctx.meta['config']
    AmsdalConfigManager().load_config(Path('./config.yml'))
    manager = AmsdalManager()
    manager.authenticate()

    try:
        manager.cloud_actions_manager.add_allowlist_ip(
            application_uuid=cli_config.application_uuid,
            application_name=cli_config.application_name,
            ip_address=ip_address,
        )
    except AmsdalCloudError as e:
        print(f'[red]{e}[/red]')
        return

    if ip_address:
        msg = (
            f'IP address/range [green]{ip_address}[/green] has been added to the allowlist. '
            'Rules should be applied in a few minutes.'
        )
    else:
        msg = 'Your IP address has been added to the allowlist. Rules should be applied in a few minutes.'

    print(msg)
