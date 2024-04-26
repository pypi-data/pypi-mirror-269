from collections import defaultdict
from pathlib import Path
from typing import Annotated

import typer
from amsdal.configs.main import settings
from amsdal.manager import AmsdalManager
from amsdal.migration.data_classes import MigrationDirection
from amsdal.migration.data_classes import MigrationFile
from amsdal.migration.data_classes import MigrationResult
from amsdal.migration.data_classes import ModuleTypes
from amsdal.migration.executors.default_executor import DefaultMigrationExecutor
from amsdal.migration.file_migration_executor import FileMigrationExecutorManager
from amsdal.migration.migrations import MigrationSchemas
from amsdal.migration.migrations_loader import MigrationsLoader
from amsdal_utils.config.manager import AmsdalConfigManager
from rich import print

from amsdal_cli.commands.build.utils.build_app import build_app
from amsdal_cli.commands.generate.enums import SOURCES_DIR
from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.constants import MIGRATIONS_DIR_NAME
from amsdal_cli.utils.cli_config import CliConfig


@sub_app.command(name='apply')
def apply(
    ctx: typer.Context,
    number: Annotated[
        str,  # noqa: RUF013
        typer.Option(
            '--number',
            '-n',
            help=(
                'Number of migration, e.g. 0002 or just 2. '
                'Use "zero" as a number to unapply all migrations including initial one.'
            ),
        ),
    ] = None,  # type: ignore[assignment]
    build_dir: Annotated[Path, typer.Option(..., '--build-dir', '-b')] = Path('.'),
    *,
    module_type: Annotated[ModuleTypes, typer.Option(..., '--module', '-m')] = ModuleTypes.APP,
    fake: Annotated[bool, typer.Option('--fake', '-f')] = False,
    config: Annotated[Path, typer.Option(..., '--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """DEPRECATED: Apply migrations."""
    print('[yellow]DEPRECATED: This command is deprecated, use `amsdal migrate` instead.[/yellow]')

    apply_callback(
        ctx,
        number,
        build_dir,
        module_type=module_type,
        fake=fake,
        config=config,
    )


@sub_app.callback(invoke_without_command=True)
def apply_callback(
    ctx: typer.Context,
    number: Annotated[
        str,  # noqa: RUF013
        typer.Option(
            '--number',
            '-n',
            help=(
                'Number of migration, e.g. 0002 or just 2. '
                'Use "zero" as a number to unapply all migrations including initial one.'
            ),
        ),
    ] = None,  # type: ignore[assignment]
    build_dir: Annotated[Path, typer.Option(..., '--build-dir', '-b')] = Path('.'),
    *,
    module_type: Annotated[ModuleTypes, typer.Option(..., '--module', '-m')] = ModuleTypes.APP,
    fake: Annotated[bool, typer.Option('--fake', '-f')] = False,
    config: Annotated[Path, typer.Option(..., '--config', '-c')] = None,  # type: ignore # noqa: RUF013
) -> None:
    """
    Apply migrations.
    """
    if ctx.invoked_subcommand is not None:
        return

    cli_config: CliConfig = ctx.meta['config']
    app_source_path = cli_config.app_directory / SOURCES_DIR

    build_app(
        app_source_path=app_source_path,
        config_path=config or cli_config.config_path,
        output=build_dir,
    )

    settings.override(APP_PATH=build_dir)
    config_manager = AmsdalConfigManager()
    config_manager.load_config(config or cli_config.config_path)
    amsdal_manager = AmsdalManager()
    amsdal_manager.setup()
    amsdal_manager.authenticate()
    amsdal_manager.post_setup()

    app_migrations_loader = MigrationsLoader(
        migrations_dir=build_dir / MIGRATIONS_DIR_NAME,
        module_type=ModuleTypes.APP,
    )
    schemas = MigrationSchemas()
    executor = FileMigrationExecutorManager(
        app_migrations_loader=app_migrations_loader,
        executor=DefaultMigrationExecutor(schemas),
    )

    if number and number.lower().strip() == 'zero':
        number = '-1'

    result: list[MigrationResult] = executor.execute(
        migration_number=int(number) if number else None,
        module_type=module_type,
        fake=fake,
    )

    if not result:
        print('[blue]Migrations are up to date[/blue]')
        return

    reverted = [item for item in result if item.direction == MigrationDirection.BACKWARD]
    applied = [item for item in result if item.direction == MigrationDirection.FORWARD]

    if reverted:
        print('[yellow]Migrations reverted[/yellow]')

        _render([item.migration for item in reverted], color='yellow')

    if applied:
        print('[green]Migrations applied[/green]')

        _render([item.migration for item in applied], color='green')


def _render(migrations: list[MigrationFile], color: str = 'yellow') -> None:
    migrations_per_type = defaultdict(list)

    for migration in migrations:
        migrations_per_type[migration.type].append(migration)

    if ModuleTypes.CORE in migrations_per_type:
        print(f'[{color}]Core:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.CORE]:
            print(f'  - [{color}]{migration.path.name}[/{color}]')

    if ModuleTypes.CONTRIB in migrations_per_type:
        print(f'[{color}]Contrib:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.CONTRIB]:
            if migration.module:
                contrib_name = '.'.join(migration.module.split('.')[:-2])
            else:
                contrib_name = 'N/A'

            print(f'  - [{color}]{contrib_name}: {migration.path.name}[/{color}]')

    if ModuleTypes.APP in migrations_per_type:
        print(f'[{color}]App:[/{color}]')

        for migration in migrations_per_type[ModuleTypes.APP]:
            print(f'  - [{color}]{migration.path.name}[/{color}]')
