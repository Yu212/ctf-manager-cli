import os

import click

from cm.utils import set_cd_path, copy_files


@click.command("init")
@click.pass_context
@click.option("-t", "--template", default="ipynb", help="Template files to use")
@click.option("-r", "--name-raw", is_flag=True, help="Use raw name")
@click.argument("name")
def init_command(ctx, template, name_raw, name):
    folder_name = name if name_raw else normalize(name)
    cwd = os.getcwd()
    folder_path = os.path.join(cwd, folder_name)
    template_dir = os.path.join("/home/yu212/PycharmProjects/cm/templates", template)
    if not os.path.exists(template_dir):
        click.echo(f"Error: Template file '{template}' does not exist.", err=True)
        return
    if os.path.exists(folder_path):
        click.echo(f"Error: Directory '{folder_name}' already exists.", err=True)
        return
    os.makedirs(folder_path)
    copy_files(template_dir, folder_path)
    set_cd_path(ctx, folder_path)
    click.echo(f"Successfully initialized directory '{folder_name}' with template '{template}'.")

def normalize(name):
    return name.replace(" ", "-").lower()
