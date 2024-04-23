""" Handling all the local docker functionalities
"""
import os
from pathlib import Path
import shutil 
from typing import Tuple

import docker
import gzip
from tqdm import tqdm
from prettytable import PrettyTable, ALL
import typer
from celestical.configuration import cli_logger
from celestical.helper import print_text

# logging.basicConfig(encoding='utf-8', level=LOGGING_LEVEL)

def get_docker_client():
    client = None
    err_msg = ""
    try:
        client = docker.from_env()
    except:
        err_msg = "Could not connect to the docker service. Is it really running?"
    return client, err_msg


def get_ports(docker_client, image_id):
    """
        Get ports from containers created from the specified image.

        returns a string for a joint list of ports
    """
    if docker_client is None:
        return ""

    ports = set()
    for container in docker_client.containers.list(all=True):
        if container.image.id == image_id:
            port_data = container.attrs['HostConfig']['PortBindings']
            if port_data:
                for port, bindings in port_data.items():
                    # get only the port number, not the protocol
                    ports.add(port.split('/')[0])
    return ', '.join(sorted(ports)) 


def list_local_images() -> Tuple[PrettyTable, str]:
    """List all docker images locally available with port information.

    Returns:
        PrettyTable of formatted table of docker images
        and an error message
    """
    docker_client, err_msg = get_docker_client()
    if docker_client == None:
        return None, err_msg

    table = PrettyTable()
    table.field_names = ["Image ID", "Image Name", "Tags", "Ports"]
    table.hrules = ALL  # Add horizontal rules between rows

    images = []
    terminal_width = 100
    try:
        terminal_width, _ = shutil.get_terminal_size()
        images = docker_client.images.list()
    except Exception as whathappened:
        # logging.error(whathappened)
        return table, err_msg

    # Adjust column widths based on the terminal width
    # divide by 2 for two lines
    id_width = max(len(image.id) for image in images) // 2 + 1
    name_width = max(len(image.tags[0].split(':')[0])
                     if image.tags
                     else 0 for image in images)
    # divide by 2 to leave space for the Ports column
    tags_width = (terminal_width - id_width - name_width - 7) // 2
    ports_width = tags_width
    table.align["Image ID"] = "l"
    table.align["Image Name"] = "l"
    table.align["Tags"] = "l"
    table.align["Ports"] = "l"
    table._max_width = {
        "Image ID": id_width,
        "Image Name": name_width,
        "Tags": tags_width,
        "Ports": ports_width}

    for image in images:
        # Split the Image ID into two lines
        half_length = len(image.id) # // 2
        formatted_id = f'{image.id[:half_length]}\n{image.id[half_length:]}'
        # Extract image name from the tags
        image_name = image.tags[0].split(':')[0] if image.tags else 'N/A'
        # Get ports
        ports = get_ports(docker_client, image.id)
        table.add_row([formatted_id, image_name, ', '.join(image.tags), ports])

    return table, err_msg


def compress_image(image_name: str, project_name: str) -> Path:
    """Compress a Docker image.
    """

    client = docker.from_env()

    save_path = Path(f"/tmp/celestical/{project_name}/")
    # Create the save_path directory and any necessary parent directories
    save_path.mkdir(parents=True, exist_ok=True)

    tar_filename = save_path / f'{image_name}.tar'
    gz_filename = save_path / f'{image_name}.tar.gz'


    # Step 1: Save the Docker image to a tar file
    # image = f'{image_name}:{tag}'
    # tar_filename = f'{image_name}_{tag}.tar'
    # with open(tar_filename, 'wb') as tar_file:
    #     for chunk in client.images.get(image).save(named=True):
    #         tar_file.write(chunk)

    print_text("Calculating total image size ..")

    # Step 1: Calculate the total size of the image
    image_data = client.images.get(image_name).save(named=True)
    total_size = sum(len(chunk) for chunk in image_data)
    total_size_mb = total_size / (1024 * 1024)


    # Reset the image data iterator
    image_data = client.images.get(image_name).save(named=True)

    print_text("\n============================================\n")
    print_text(f"Image Name:Tag: {image_name} \t Image Size: {total_size_mb:.2f} MB")
    print_text(f"Saving in: {save_path} \t File Name: {gz_filename}")
    # print_text(f"App context: {context} \t Domain: {domain}")
    print_text("\n============================================\n")

    # Prompt user for confirmation before proceeding with compression
    if not typer.confirm("Would you like to proceed with saving and compressing the image?"):
        print_text("Aborting the program.")
        raise typer.Abort()

    print_text("Starting to save the image .. ")
    # Save the Docker image to a tar file with a progress bar
    with open(tar_filename, 'wb') as tar_file:
        with tqdm(total=total_size, unit='B', unit_scale=True, desc='Saving') as pbar:
            for chunk in image_data:
                tar_file.write(chunk)
                pbar.update(len(chunk))

    print_text("Compressing exported tar image (gzip)...")

    # Step 2: Compress the tar file using gzip
    file_size = os.path.getsize(tar_filename)
    with open(tar_filename, 'rb') as tar_file:
        with gzip.open(gz_filename, 'wb') as gz_file:
            with tqdm(total=file_size, unit='B', unit_scale=True, desc='Compressing') as pbar:
                # Define a chunk size (e.g., 1 MiB)
                chunk_size = 1024 * 1024
                # Read, compress, and write data in chunks
                while chunk := tar_file.read(chunk_size):
                    gz_file.write(chunk)
                    pbar.update(len(chunk))

    print_text("\n============================================\n")
    print_text(f"Image {image_name} compressed successfully in {save_path}!")
    print_text("\n============================================\n")

    return gz_filename
