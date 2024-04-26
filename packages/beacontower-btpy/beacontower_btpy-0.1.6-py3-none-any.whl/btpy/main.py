import typer

from btpy.commands import env_commands

app = typer.Typer()

app.add_typer(env_commands.app, name="env")

if __name__ == "__main__":
    app()
