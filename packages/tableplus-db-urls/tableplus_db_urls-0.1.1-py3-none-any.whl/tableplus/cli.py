import logging
from pathlib import Path

import click

from .core import get_local_db_conn_str
from .core import get_prod_db_conn_str

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def silent_echo(*args, **kwargs):
    pass


@click.command()
@click.option("-p", "--path", required=True, help="Path to the project")
@click.option("--ssh-user", required=True, help="SSH User")
@click.option("--ssh-host", required=True, help="SSH Host")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def generate(path, ssh_user, ssh_host, verbose) -> None:
    """Main entry point for the CLI."""

    if not verbose:
        click.echo = silent_echo

    project_path = Path(path).expanduser()
    local_env_path = str(project_path / ".envs/.local/.postgres")
    prod_env_path = str(project_path / ".envs/.production/.postgres")

    local_db_url = get_local_db_conn_str(local_env_path)
    prod_db_url = get_prod_db_conn_str(prod_env_path, ssh_user, ssh_host)

    click.secho("=> TablePlus: Right click > New > Connection from URL...", fg="green")
    click.secho("\nLOCAL:", dim=True)
    click.secho(f"{local_db_url}")
    click.secho("\nPROD:", dim=True)
    click.secho(f"{prod_db_url}")


# Set up your command-line interface grouping
@click.group()
@click.version_option(package_name="tableplus-db-urls", prog_name="tableplus-db-urls")
def cli():
    """Generate TablePlus DB URLs from CookieCutter Django to make setting
    up connections easier."""


cli.add_command(generate)

if __name__ == "__main__":
    cli()
