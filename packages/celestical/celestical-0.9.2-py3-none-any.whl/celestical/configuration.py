# Managing the configuration for the Celestical services
import json
import os
import logging
from logging import Logger
from pathlib import Path

import typer
from prettytable import PrettyTable, ALL

import celestical.api as api
from celestical.helper import print_text

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
apiconf = api.Configuration(
        host = "http://localhost:8000"
)

# LOGGING_LEVEL = logging.DEBUG
# logging.basicConfig(encoding='utf-8', level=LOGGING_LEVEL)

HOTLINE = "starship@celestical.net"
PRODUCTION = False


def get_default_config_dir() -> Path:
    path = Path.home() / ".config" / "celestical" 
    return path


def get_default_config_path() -> Path:
    """Return the default config path for this application

    Returns:
        Path typed path to the config json file
    """
    path = get_default_config_dir() / "config.json"
    return path


def get_default_log_path() -> Path:
    """Return the default log file path for this application

    Returns:
        Path typed path to the log file
    """
    path = get_default_config_dir() / "celestical.log"
    return path


def load_config(config_path: str = "") -> dict:
    """Load config file from config_path.

    Params:
        config_path(str): non-default absolute path of the configuration.
    Returns:
        (dict): configuration content
    """
    path = get_default_config_path()
    if config_path is not None and config_path != "":
        path = Path(config_path)

    user_data = {}
    if path.exists():
        try:
            with open(path, 'r') as f_desc:
                user_data = json.load(f_desc)
        except:
            print_text("Could not read the configuration file.")
    else:
        print_text("The configuration file does not exist yet.")

    return user_data


def save_config(config:dict):
    """Save config file to the default_config_path.

    Params:
        config(dict): configuration.
    Returns:
        (str): configuration absolut path
    """
    cpath = get_default_config_path()

    try:
        if not cpath.parent.exists():
            os.makedirs(cpath.parent, exist_ok=True)
    except Exception as e:
        typer.echo("Config directory couldn't be created successfully")

    with open(cpath, 'w') as f:
        json.dump(config, f, indent=4)

    typer.echo(f"Login credentials safely updated in: {cpath}")
    return cpath


def cli_setup() -> bool:
    """ Setup necessary directories.
    """
    config_path = get_default_config_dir()
    try:
        config_path.mkdir(parents=True, exist_ok=True)
    except Exception as oops:
        return False
    return True


def create_logger(production: bool=False) -> Logger :
    """A function to create and configure the logger for the Celestical CLI
    Params:
        production(bool): if False, set log level to debug
    Returns:
        (logger): the logger object
    """
    log_format = "%(asctime)s --%(levelname)s: %(message)s"
    log_location = get_default_log_path()
    if production is False:
        logging.basicConfig(
            encoding='utf-8',
            filename=log_location,
            format=log_format,
            filemode="a",
            level=logging.DEBUG,
        )
        logger = logging.getLogger(name="Celestical CLI")
        logger.warning(f"Starting Logger in DEBUG Mode: {log_location}")
        return logger
    
    logging.basicConfig(
        encoding='utf-8',
        filename=log_location,
        format=log_format,
        filemode="a",
        level=logging.WARNING,
    )
    logger = logging.getLogger(name="Celestical CLI")
    logger.warning(f"Starting Logger in WARNING Mode: {log_location}")
    return logger

cli_setup()
# Creation of the CLI-wide logger -> celestical.log
cli_logger = create_logger(production=PRODUCTION)
