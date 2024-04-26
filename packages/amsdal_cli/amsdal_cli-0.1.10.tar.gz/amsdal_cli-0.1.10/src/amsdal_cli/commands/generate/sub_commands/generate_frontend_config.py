import json
from pathlib import Path

import typer
from amsdal.contrib.frontend_configs.lifecycle.consumer import get_default_control
from amsdal.manager import AmsdalManager
from amsdal_models.schemas.loaders.cli_fixtures_loader import FIXTURES
from amsdal_utils.config.manager import AmsdalConfigManager
from amsdal_utils.utils.text import to_snake_case
from rich import print

from amsdal_cli.commands.generate.app import sub_app
from amsdal_cli.commands.generate.utils.build_base_path import build_model_base_path
from amsdal_cli.utils.cli_config import CliConfig
from amsdal_cli.utils.copier import write_file


@sub_app.command(name='frontend_config')
def generate_frontend_config(
    ctx: typer.Context,
    model: str = typer.Option(..., help='The model name. It should be provided in PascalCase.'),
) -> None:
    """
    Generates Frontend Config fixture file for specified model.
    """
    cli_config: CliConfig = ctx.meta['config']
    config_manager = AmsdalConfigManager()
    config_manager.load_config(cli_config.config_path)
    amsdal_manager = AmsdalManager()
    amsdal_manager.pre_setup()

    try:
        target_fixture = {
            'FrontendModelConfig': [
                {
                    'external_id': f'{to_snake_case(model)}_frontend_config',
                    'class_name': model,
                    'control': get_default_control(model),
                }
            ]
        }
    except ModuleNotFoundError as e:
        print(f'[red]Model {model} not found. Please conside building the app first.[/red]')
        raise typer.Exit from e

    base_path = build_model_base_path(ctx, model)
    (base_path / FIXTURES).mkdir(parents=True, exist_ok=True)
    frontend_config_file = base_path / FIXTURES / 'ui.json'
    current_dir = Path('.').absolute()

    if frontend_config_file.exists():
        owerrite = input(
            f'The file "{frontend_config_file.relative_to(current_dir)}" already exists. '
            'Would you like to overwrite it? [y/N]: '
        ).strip()

        if owerrite.lower() != 'y':
            return

    write_file(
        json.dumps(target_fixture, indent=cli_config.json_indent),
        destination_file_path=frontend_config_file,
        confirm_overwriting=False,
    )
