import click
from .export import main


@click.command()
@click.option(
    "-e",
    "--env",
    help="env file, default is .env",
)
@click.option(
    "-f",
    "--config-file",
    default="config.toml",
    help="configuration file (default is ./config.toml)",
)
@click.option(
    "-u",
    "--username",
    help="username for troopwebhost",
)
@click.option(
    "-t",
    "--troop-id",
    help="troop id (find this from troopwebhost)",
)
def main_func(env=None, config_file=None, username=None, troop_id=None):
    main(env, config_file, username, troop_id)


if __name__ == "__main__":
    main()
