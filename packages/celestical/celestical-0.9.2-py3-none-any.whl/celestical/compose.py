""" File to manage docker compose file and their enrichment """
import sys
from pathlib import Path
from typing import Tuple

import uuid
import yaml
import typer
import docker

import celestical.api as api
from celestical.api.exceptions import UnauthorizedException
from celestical.api import (
    App,
    Compose)

from celestical.user import (
    user_login,
    user_register,
    load_user_creds)

from celestical.docker_local import \
    compress_image

from celestical.helper import (
    cli_panel,
    prompt_user,
    confirm_user,
    print_text,
    print_feedback,
    guess_service_type_by_name,
    save_yaml,
    SERVICE_TYPES)

from celestical.configuration import (
    HOTLINE,
    apiconf,
    cli_logger,
    load_config)


def get_image_hash(image_name_tag:str) -> str:
    """Get the hash for a certain docker image name and tag."""

    client = docker.from_env()
    image = client.images.get(image_name_tag)
    return image.id


def get_ports(image_id, docker_client):
    """Get ports from containers created from the specified image."""
    ports = set()
    for container in docker_client.containers.list(all=True):
        if container.image.id == image_id:
            port_data = container.attrs['HostConfig']['PortBindings']
            if port_data:
                for port, bindings in port_data.items():
                    # get only the port number, not the protocol
                    ports.add(port.split('/')[0])
    return ', '.join(sorted(ports))


def richformat_services(services:dict) -> str:
    """Create a rich formatted string to display a bullet list for services
    """
    s_info = ""
    for serv in services:
        if "image" not in services[serv]:
            services[serv]["image"] = "-undefined-"
        s_info += f"\t- [yellow]{serv}[/yellow] (image)--> "
        s_info += f"{services[serv]['image']}\n"
    return s_info


def read_docker_compose(fullpath: Path) -> dict:
    """Read the docker-compose.yml file.

    Params:
        fullpath(Path): absolut path to the docker-compose.yml file
    Returns:
        (dict): docker-compose.yml file content
    """

    compose = None
    try:
        with open(fullpath, 'r') as f:
            compose = yaml.safe_load(f)
    except FileNotFoundError:
        msg = f"No file found at given path: {fullpath}"
        print_text(msg)
        cli_logger.error(msg)
    return compose


def enrich_compose(
    compose: dict,
    prev_comp:dict = {},
    ecomp_path:Path = None) -> Path:
    """Enrich a stack with additional information about the services.
    Params:
        compose(dict): docker-compose.yml file content
    Returns:
        (dict): enriched docker-compose.yml file content
    """
    enriched_compose: dict = compose
    services: list = compose.get('services', {})

    # init an empty enrichment metadata
    enriched_compose["celestical"] = {}

    # extracting default values that could be set here
    def_app_name:str|None = None
    def_base_domain:str|None = None
    if prev_comp is not None and isinstance(prev_comp, dict):
        if "celestical" in prev_comp:
            def_app_name = prev_comp["celestical"].get(
                "name",
                None)
            def_base_domain = prev_comp["celestical"].get(
                "base_domain",
                None)


    # metadata: Appplication name
    # app_name: str = prompt_user(
    #     "Name for your App",
    #     default=def_app_name)
    # app_name = app_name.strip()

    # # TODO clean name of whitespaces
    # enriched_compose["celestical"]["name"] = app_name
    # print_feedback(enriched_compose["celestical"]["name"])

    # metadata: base domain
    base_domain: str = prompt_user(
        f"Indicate the base domain for your app?\n"
        +f"     (e.g.  myapp.parametry.ai or parametry.ai)",
        default=def_base_domain,
        helptxt="If the base domain is a subdomain, it would constitute "
            +"your base domain, e.g.: app2.celestical.net\n")
    base_domain = base_domain.strip()
    base_domain = base_domain.lower()
    if "http://" in base_domain or "https://" in base_domain:
        base_domain = base_domain.split("://")[-1]
    enriched_compose["celestical"]["base_domain"] = base_domain
    enriched_compose["celestical"]["name"] = base_domain
    print_feedback(enriched_compose["celestical"]["base_domain"])

    # summarizing current services in docker compose file
    msg = "[underline]Here is a quick recap[/underline]\n\n"
    msg += f"Your App: [green]{enriched_compose['celestical']['name']}[/green]\n"
    msg += f"Website: [green]https://{enriched_compose['celestical']['base_domain']}[/green]\n"
    msg += "runs the following services:\n"
    msg += richformat_services(services)
    msg += "\n\n[yellow]We will tag services by usage tag[/yellow]:\n"

    serveme_types = [serv for serv in SERVICE_TYPES]
    help_on_types = "Type the type number or name\n"
    for n in range(len(serveme_types)):
        help_on_types += f"\t{n+1} --> {serveme_types[n]}\n"

    cli_panel(msg+help_on_types)

    counter: int = 1
    for service_name in services:
        # --- display current service name and guessed type
        msg = f"Choose a type for service #{counter} of {len(services)}: "
        msg += f"[yellow]{service_name}[/yellow] --> "

        img_name = services[service_name].get("image", "")
        stype = guess_service_type_by_name(service_name, img_name)
        msg += f" detected type: [purple]{stype}[/purple]"

        # --- ask for a better categorization
        prompt_done = False
        while prompt_done is False:
            type_nbr:str = prompt_user(msg, default=stype, helptxt=help_on_types)
            type_nbr = type_nbr.strip()
            type_nbr = type_nbr.upper()
            prompt_done = True
            match type_nbr:
                case "1":
                    stype = serveme_types[0]
                case "2":
                    stype = serveme_types[1]
                case "3":
                    stype = serveme_types[2]
                case "4":
                    stype = serveme_types[3]
                case "5":
                    stype = serveme_types[4]
                case _:
                    # type_nbr might be something else
                    if type_nbr == "":
                        #stype is already set
                        prompt_done = True
                    elif type_nbr in SERVICE_TYPES:
                        stype = type_nbr
                        prompt_done = True
                    else:
                        prompt_done = False

        enriched_compose["services"][service_name]["celestical_type"] = stype
        print_feedback(
            enriched_compose["services"][service_name]["celestical_type"])

        msg = f"[underline]Public URL[/underline] for service [yellow]{service_name}[/yellow] "
        service_url: str = prompt_user(msg, default="", helptxt="Leave empty if none")

        if service_url != "":
            enriched_compose["services"][service_name]["celestical_url"] = service_url
            print_feedback(
                enriched_compose["services"][service_name]["celestical_url"])

        # TODO get image hash or not
        # enriched_compose["services"][service_name]["celestical_image_hash"] = service_name["image"]
        counter += 1

    save_path: Path = save_yaml(data=enriched_compose, yml_file=ecomp_path)
    return save_path


def check_for_enrichment(compose_path:str) -> Tuple[Path, dict, dict]:
    """ Find the compose file in the given folder if it is a folder and decide
    where the enriched compose file will be. Check with the user if enrichment
    is necessary when already present

        Returns: three elements:
         - the path to the found most recent docker-compose or enriched
        file
         - the python dictionary of that most recent compose file content with
           first metadata containing info if user wants to enrich or not.
           From confirmation ask thanks to timestamp comparison.
         - the python dictionary of the enriched file anyway found, so it can be
           used for default values while enrichiing to fasten and ease the
           process.
    """

    # use current directory if nothing provided
    docker_compose_path = Path.cwd()
    docker_ecompose_path = Path.cwd() / 'docker-compose-enriched_dpath.yml'
    if compose_path is not None:
        if compose_path != "":
            docker_compose_path = Path(compose_path)

    # if we get a directory, complete full path
    selected_path = None
    prev_compose = {}
    if docker_compose_path.is_dir():
        docker_ecompose_path = docker_compose_path / \
          'docker-compose-enriched.yml'
        docker_compose_path = docker_compose_path / 'docker-compose.yml'
    elif docker_compose_path.is_file():
        # we consider docker_compose_path a valid file set from user
        # We try to find the enriched file
        file_dir = docker_compose_path.parent
        docker_ecompose_path = file_dir / 'docker-compose-enriched.yml'
    else:
        # provided path is neither a directory or file, e_xit.
        cli_panel("docker-compose.yml file is not a valid file:\n"
                 +f"{docker_compose_path}\n\n"
                 +"Give another docker-compose path on command line: \n"
                 +"\t=> [yellow]celestical deploy "
                 +"/path/to/docker-compose.yml[/yellow]")
        cli_logger.debug("exiting as provider docker compose path is wrong")
        sys.exit(4)

    # --- selecting most recent valid path
    comp_time = 1.0
    if docker_compose_path.is_file():
        comp_time = docker_compose_path.stat().st_mtime

    ecomp_time = 0.0
    if docker_ecompose_path.is_file():
        prev_compose = read_docker_compose(fullpath=docker_ecompose_path)
        ecomp_time = docker_ecompose_path.stat().st_mtime

    if ecomp_time > comp_time:
        selected_path = docker_ecompose_path
    else:
        selected_path = docker_compose_path

    # --- selected process compose file
    if selected_path.is_file():
        c_dict = read_docker_compose(fullpath=selected_path)

        s_info = "\n* Services found in detected docker-compose file: \n"
        s_info += f"\t[green]{selected_path}[/green]\n\n"

        if "services" in c_dict:
            s_info += richformat_services(c_dict["services"])

        if "celestical" in c_dict:
            s_info += f"\n* [underline]App name[/underline]: " \
                     +f"[green]{c_dict['celestical']['name']}[/green]\n"
            s_info += f"* [underline]App URL[/underline]: " \
                     +f"[blue]{c_dict['celestical']['base_domain']}[/blue]\n\n"



        cli_panel(s_info)

        if "celestical" in c_dict:
            msg = "(Yes) To deploy now | (No) To reset info"
            answer = confirm_user(msg, default=True)

            if answer:
                # Skip enrichment
                c_dict["celestical"]["skip_enrich"] = True
                return docker_ecompose_path, c_dict, prev_compose
            # else will lead to enrichment (reset)
            c_dict["celestical"]["skip_enrich"] = False
            return docker_ecompose_path, c_dict, prev_compose

        answer = confirm_user("Continue with this file", default=True)
        if answer:
            return docker_ecompose_path, c_dict, prev_compose
        # else we exit for another file
        cli_panel("Give another path on command line: \n"
                 +"\t=> celestical deploy /path/to/docker-compose.yml")
        sys.exit(0)
    else:
        cli_panel("No docker-compose.yml file was found at:\n"
                 +f"{selected_path}\n\n"
                 +"Give another docker-compose path on command line: \n"
                 +"\t=> [yellow]celestical deploy /path/to/docker-compose.yml[/yellow]")
        cli_logger.debug("exiting as no docker compose file found")
        sys.exit(2)

    return None, None, {}


def upload_images(app_uuid:uuid.UUID, compose_path:Path|None=None, e_compose:dict|None=None) -> bool:
    """Upload the enriched compose file to the Celestical Cloud."""

    cli_panel("Let's start uploading your App's images to Celestical")

    if compose_path is not None:
        e_compose = read_docker_compose(fullpath=compose_path)
    elif e_compose is None:
        return False 

    # Build the compressed tar file for each service
    image_paths = []
    for service_name in e_compose["services"]:
        # typer.echo(service_name)
        #typer.confirm("Do you wish to proceed setting the image_name?")
        #image_name = e_compose["services"][service_name]["image"].split(':')[0]
        image_name = e_compose["services"][service_name]["image"]
        #typer.echo(image_name)
        #typer.confirm("Do you wish to proceed compressing?")
        ipath = compress_image(image_name=image_name, project_name=e_compose["celestical"]["name"])
        image_paths.append(ipath)

    api_ires = None
    with api.ApiClient(apiconf) as api_client:
        app_api = api.AppApi(api_client)

        for ipath in image_paths:
            try:
                with ipath.open(mode="rb") as ipath_desc:
                    # upfile = {"file": ipath.name, ipath_desc, "multipart/form-data")}
                    upfile = {"file": ipath_desc}
                    cli_logger.debug("Making compose info push request")
                    api_ires = app_api.upload_image_compressed_file_app_app_uuid_upload_image_post( \
                        app_uuid=app_uuid,
                        image_file=upfile)

            except Exception as oops:
                cli_logger.debug(oops)
                pass


def upload_compose(compose_path:str, call_nbr:int = 1) -> dict:
    """ This function find the compose file and ask the user for enrichment
        unless an enriched file is already present in case user is asked
        if they want to reset the enrichment.

        - compose_path:str: string of the folder to deploy, it should contain
          a docker compose file. It is where the enriched file will be saved
        - call_nbr:str: in case we are missing authentication we are trying to
          login again to get a new token. If that does not work something else
          is going on.
    """
    # --- Find file and verify path and previous enrichment
    ecomp_path, comp_dict, prev_comp = check_for_enrichment(compose_path)

    do_enrich:bool = True
    if "celestical" in comp_dict:
        if "skip_enrich" in comp_dict["celestical"]:
            if comp_dict["celestical"]["skip_enrich"] is True:
                do_enrich = False

    # --- Get info from user to enrich context
    enriched_compose = {}
    if do_enrich:
        enriched_compose = enrich_compose(comp_dict, prev_comp, ecomp_path)
    else:
        enriched_compose = comp_dict

    # --- Posting the body package for Compose file
    compose_pack = {}
    compose_pack["enriched_compose"] = enriched_compose
    # optional in case we want to upload compose for later deployment
    compose_pack["deploy"] = True

    setcred, mesg = load_user_creds(apiconf)
    if setcred is False:
        cli_panel(msg)
        return None

    api_response = None
    with api.ApiClient(apiconf) as api_client:
        app_api = api.AppApi(api_client)

        try:
            # App creation with compose (possibly empty) upload
            cli_logger.debug("Preparing compose info to post")
            compose_to_post = Compose.from_dict(compose_pack)

            cli_logger.debug("Making compose info push request")
            api_response = app_api.upload_compose_file_app_compose_post( \
                compose_to_post)

        except UnauthorizedException as oops:
            # Let's try to relog again and relaunch that function
            if call_nbr > 1:
                msg = "Please check your connection and credentials\n"
                msg += "[red]no access authorized for now[/red]\n\n"
                msg += "You might need to register with: "
                msg += "[yellow]celestical register[/yellow]\n\n"
                msg += "If problem persists please contact us: {HOTLINE}"
                cli_panel(msg)
                return None
            # else
            cli_panel("You have to log in again, your token may have expired." \
                      +" (signing out automatically)")
            user_login(force_relog=True)
            call_nbr += 1
            cli_logger.debug(oops)
            return upload_compose(compose_path, call_nbr)
        except Exception as oops:
            cli_panel("Something undefined happened: Check your connection.")
            cli_logger.error("Error during post of enriched compose file")
            cli_logger.error(oops)
            return None

    if (not isinstance(api_response, App)):
        cli_logger.error("API response is not an App.")
        msg = "Try to login again, your token might have expired.\n"
        msg += "--> [underline]celestical login[/underline]"
        cli_panel(msg)
        return None

    # at this point api_response is an App
    if "celestical" in enriched_compose:
        enriched_compose["celestical"]["app_id"] = str(api_response.id)
        save_path: Path = save_yaml(data=enriched_compose, yml_file=ecomp_path)

    return enriched_compose
