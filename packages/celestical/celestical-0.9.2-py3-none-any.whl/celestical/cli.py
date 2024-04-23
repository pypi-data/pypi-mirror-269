"""The CLI to interface with the Celestical Serverless Cloud."""
import logging
from logging import Logger
from typing import Optional
from typing_extensions import Annotated

import typer

from celestical.compose import (
    upload_compose,
    upload_images)
from celestical.docker_local import list_local_images
from celestical.helper import cli_panel, welcome_message
from celestical.configuration import cli_logger
from celestical.user import user_login, user_register
from celestical.apps import list_creator_apps


cli_logger.info("Starting CLI.")

app = typer.Typer(pretty_exceptions_short=False,
                  no_args_is_help=True,
                  help=welcome_message,
                  rich_markup_mode="rich")
cli_logger.debug("Typer created successfully.")

# @app.callback(invoke_without_command=True)
@app.command()
def apps():
    """List all apps from current user."""
    list_creator_apps()


@app.command()
def login() -> None:
    """Login to Parametry's Celestical Cloud Services via the CLI."""
    cli_logger.debug("Entering the login function")
    user_login()


@app.command()
def register():
    """Register as a user for Celestical Cloud Services via the CLI."""
    user_register()


@app.command()
def images():
    """ List all local docker images for you.
        Similar to 'docker image ls'.
    """
    table, err_msg = list_local_images()

    if table is None or err_msg != "":
        cli_panel("Docker service is [red]unaccessible[/red]\n\n"
                 +f"{err_msg}")
    else:
        cli_panel("The following are your local docker images\n"
                 +f"{table}")


@app.command()
def deploy(compose_path: Annotated[Optional[str], typer.Argument()] = "./"):
    """Compress and upload a Docker image to the Celestical Cloud."""
    # --- First the compose enrichment:
    # 1- find compose file
    # 2- enrich it
    enriched_compose = upload_compose(compose_path)

    # --- Upload images according to response
    # 1- read response, and feedback user on status
    # 2- if 200, select the list of images in response.
    # 3- compress concerned images
    # 4- upload concerned images
    # .. keep feedback to user whenever progress is made
    if enriched_compose is None:
        cli_panel("Stopping here - could not enriched compose file")
        return

    upload_images(app_uuid=enriched_compose["celestical"]["app_id"], e_compose=enriched_compose)


