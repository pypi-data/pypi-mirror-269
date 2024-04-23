""" user related functions

    This file holds the routines to login, register
    and manage user data and configuration.
"""
import getpass
from datetime import datetime
from typing import Tuple

from celestical.api import (
    ApiClient,
    AuthApi,
    ApiException,
    UserCreate)
from celestical.configuration import (
    apiconf,
    load_config,
    save_config,
    cli_logger)
from celestical.helper import (
    cli_panel,
    prompt_user,
    confirm_user)


def login_form(ask:str = "Please enter your wonderful Celestical credentials",
    default_email:str = None
    ) -> Tuple[str, str]:
    cli_panel(ask)
    user_mail = prompt_user("User Mail", default=default_email)
    if "@" not in user_mail:
        cli_logger.error("Entered email address is missing a '@'")
        cli_panel(message="Email is incorrect: no @ sign found.", _type="error")
        return login_form(ask)

    password = getpass.getpass(" *** Password: ")
    cli_logger.info("Password succesfully created.")

    if len(password) <= 7:
        cli_logger.error("Password is too short!")
        cli_panel(message="Password too short!", _type="error")
        return login_form(ask)
    return (user_mail, password)


def user_login(default_email:str = None,
               force_relog:bool = False,
               ) -> bool:
    """Login to Parametry's Celestical Cloud Services via the CLI.

    Returns:
        bool
    """
    cli_logger.info("Entering user login function in user.py")
    user_data = {}
    if default_email is None:
        user_data = load_config()

    use_user = False
    if "access_token" in user_data:
        if len(user_data["access_token"]) > 10:
            if "username" not in user_data:
                cli_logger.warning("Oh no it seems config was manually edited.")
            elif force_relog == False:
                cli_panel(f"You are logged in as {user_data['username']}")
                use_user = confirm_user("Do you want to continue" \
                    + f" with user [yellow]{user_data['username']}[/yellow]")
                if use_user:
                    cli_panel("\t --> continuing as " \
                        +f"[yellow]{user_data['username']}[/yellow]")
                    return True

        if force_relog:
            # Similar to a logout: forgetting token
            data = {
                "created": datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S'),
                "username": "",
                "access_token": "",
                "token_type": ""
            }
            save_config(data)

            if "username" in user_data:
                if user_data['username'] is None or user_data['username'] == "":
                    return user_login(default_email=None)
                # else we've got a previous email info
                return user_login(default_email=user_data['username'])
            return user_login()

    with ApiClient(apiconf) as api_client:
        # Create an instance of the API class
        api_instance = AuthApi(api_client)

        (username, password) = login_form(default_email=default_email)

        try:
            # Auth:Jwt.Login
            api_response = api_instance.auth_jwt_login_auth_jwt_login_post(username, password)
            cli_logger.debug("we did get a api response")
            if api_response.token_type != "bearer":
                cli_logger.debug("This client does not handle non bearer type token")
                return False

            if len(api_response.access_token) < 10:
                cli_logger.debug("Received token seems invalid")
                return False

            # Collect all user data and save it
            cli_logger.debug("Creating and saving user data/conf.")
            data = {
                "created": datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S'),
                "username": username,
                "access_token": api_response.access_token,
                "token_type": api_response.token_type
            }
            save_config(data)
        except ApiException as api_exp:
            cli_logger.error("Code Enceladus: ApiException when logging in.")
            cli_logger.debug(api_exp)
            cli_panel("Sorry we could not log you in at the moment")
            return False
        except Exception as oops:
            cli_logger.error("Code Mars: could not connect, try again after checking your connection.")
            cli_logger.debug(oops)
            return False

    return True


def user_register() -> bool:
    """Register as a user for Parametry Cloud Services via the CLI."""

    with ApiClient(apiconf) as api_client:
        auth = AuthApi(api_client=api_client)

        (user_mail, password) = login_form("Please enter new Celestical credentials")

        apires = None
        try:
            apires = auth.register_register_auth_register_post(
                    user_create=UserCreate(
                        email= user_mail,
                        password=password
                        )
                    )
        except ApiException as api_err:
            msg = f"---- Registration error ({api_err.status})"
            cli_logger.error(msg)
            cli_logger.debug(apires)
            if api_err.body:
                cli_logger.debug(api_err.body)
            else:
                cli_logger.debug(api_err.reason)
            return False

        cli_panel("You are now registered and must verify your email")
        return True


def load_user_creds(_apiconf) -> Tuple[bool, str]:
    """ Reads user creds from config and set access token 

        _apiconf from api.Configuration()
        is set with latest access token.
    """
    user_data = load_config()

    if user_data is not None and isinstance(user_data, dict):
        # cover the case of an apiKey type security
        _apiconf.api_key['Authorization'] = \
          user_data.get("access_token", "")
        _apiconf.api_key_prefix['Authorization'] = \
          user_data.get("token_type", "bearer")
        # cover the case of an http+bearer type security
        # (this is current default on celestical's API side
        _apiconf.access_token = user_data.get("access_token", "")
        return True, "Loaded creds for API request"

    msg = "[red]Could not upload you deployment config you need to login first[/red]\n"
    msg += "--> [underline]celestical login[/underline]"
    return False, msg

