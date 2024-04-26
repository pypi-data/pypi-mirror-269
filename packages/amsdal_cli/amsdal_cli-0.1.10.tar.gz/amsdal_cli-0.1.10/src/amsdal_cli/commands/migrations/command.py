from amsdal_cli.app import app
from amsdal_cli.commands.migrations.app import sub_app
from amsdal_cli.commands.migrations.sub_commands import *  # noqa

app.add_typer(sub_app, name='migrate')
app.add_typer(sub_app, name='migrations')
