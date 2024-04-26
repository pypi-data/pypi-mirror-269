from pathlib import Path
from typing import Annotated

import typer
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.migration.data_classes import MigrationFile
from amsdal.migration.file_migration_generator import FileMigrationGenerator
from amsdal.migration.schemas_loaders import JsonClassSchemaLoader
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.utils.text import to_snake_case
from rich import print

from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.command(name='make')
def make(
    ctx: typer.Context,
    build_dir: Annotated[Path, typer.Option('--build-dir', '-b')] = Path('.'),
    *,
    name: Annotated[str, typer.Option('--name', '-n', help='Migration name')] = None,  # type: ignore # noqa: RUF013
    is_data: Annotated[bool, typer.Option('--data', '-d', is_flag=True, help='Create data migration')] = False,
    config: Annotated[Path, typer.Option('--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """
    Create schema migration based on the changes in the models' schemas
    or create an empty data migration using --data flag.
    """
    cli_config: CliConfig = ctx.meta['config']

    settings.override(APP_PATH=build_dir)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config or cli_config.config_path)
    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.post_setup()

    app_source_path = cli_config.app_directory / SOURCES_DIR
    schema_loader = JsonClassSchemaLoader(app_source_path / 'models')
    migrations_dir: Path = cli_config.app_directory / SOURCES_DIR / MIGRATIONS_DIR_NAME

    generator = FileMigrationGenerator(
        schema_loader=schema_loader,
        app_migrations_path=migrations_dir,
    )

    try:
        name = to_snake_case(name) if name else None  # type: ignore[assignment]
        migration: MigrationFile = generator.make_migrations(
            name=name,
            is_data=is_data,
        )
    except UserWarning as warn:
        print(f'[blue]{warn}[/blue]')
    else:
        print(f'[green]Migration created: {migration.path.name}[/green]')
