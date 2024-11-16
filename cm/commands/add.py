import os
import re
import shutil
import tarfile
from urllib.parse import urlparse
from zipfile import ZipFile
import tempfile

import click
import requests
from requests import RequestException

from cm.utils import copy_file_or_directory, is_url


@click.command("add")
@click.argument("source")
@click.option("--no-extract", is_flag=True, help="Do not extract the file")
@click.option("--no-flatten", is_flag=True, help="Do not flatten the file")
def add_command(source, no_extract, no_flatten):
    cwd = os.getcwd()
    if is_url(source):
        destination_path = download_file(source, cwd)
        if not destination_path:
            return
    else:
        if not os.path.exists(source):
            click.echo(f"Error: Source path '{source}' does not exist.", err=True)
            return
        basename = os.path.basename(source)
        destination_path = os.path.join(cwd, basename)
        if os.path.exists(destination_path):
            click.echo(f"Error: '{basename}' already exists in the current directory.", err=True)
            return
        copy_file_or_directory(source, destination_path)
    if not no_extract:
        if no_flatten:
            file_basename = os.path.basename(destination_path)
            folder_name = extract_dest_path(file_basename)
            extract_dest = os.path.join(cwd, folder_name)
            if os.path.exists(extract_dest):
                click.echo(f"Error: '{folder_name}' already exists in the current directory.", err=True)
                return
            extract_file(destination_path, extract_dest)
        else:
            with tempfile.TemporaryDirectory(delete=True) as extract_dest:
                extract_file(destination_path, extract_dest)
                flatten_and_move(extract_dest, cwd)

def extract_dest_path(file_basename):
    folder_name = os.path.splitext(file_basename)[0]
    if file_basename.endswith(".tar.gz"):
        folder_name = folder_name.removesuffix(".tar")
    return folder_name

def flatten_and_move(src, dest):
    while True:
        contents = os.listdir(src)
        if len(contents) == 1 and os.path.isdir(os.path.join(src, contents[0])):
            src = os.path.join(src, contents[0])
        else:
            break
    for item in os.listdir(src):
        item_path = os.path.join(src, item)
        shutil.move(item_path, dest)
    click.echo(f"Flattening complete at: {dest}")

def download_file(url, dest_folder):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_disp = response.headers.get("Content-Disposition", "")
        filenames = re.findall("filename=\"(.+)\"", content_disp)
        if filenames:
            filename = filenames[0]
        else:
            filename = os.path.basename(urlparse(url).path)
        dest_path = os.path.join(dest_folder, filename)
        if os.path.exists(dest_path):
            click.echo(f"Error: '{filename}' already exists in the current directory.", err=True)
            return None
        with open(dest_path, "wb") as f:
            with click.progressbar(response.iter_content(chunk_size=8192), label="Downloading file...") as bar:
                for chunk in bar:
                    f.write(chunk)
        return dest_path
    except RequestException as e:
        click.echo(f"Error downloading file: {e}", err=True)
        return None

def extract_file(file_path, extract_to):
    try:
        if file_path.endswith(".zip"):
            click.echo(f"extracting {file_path}")
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
            with ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(extract_to)
        if file_path.endswith((".tar.gz", ".tgz")):
            click.echo(f"extracting {file_path}")
            if not os.path.exists(extract_to):
                os.makedirs(extract_to)
            with tarfile.open(file_path, "r:gz") as tar_ref:
                tar_ref.extractall(extract_to)
        else:
            return False
        return True
    except Exception as e:
        click.echo(f"Error extracting file: {e}", err=True)
        return False
