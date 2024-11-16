import os

import click
from click import pass_context

from cm.utils import set_cd_path


@click.command("solved")
@pass_context
def solved_command(ctx):
    cwd = os.getcwd()
    dir_name = os.path.basename(cwd)
    if dir_name.endswith("-solved"):
        click.echo("Error: Directory is already marked as solved.", err=True)
        return
    new_name = dir_name + "-solved"
    new_dir_path = rename_current_directory(new_name)
    set_cd_path(ctx, new_dir_path)

@click.command("unsolved")
@pass_context
def unsolved_command(ctx):
    cwd = os.getcwd()
    dir_name = os.path.basename(cwd)
    if not dir_name.endswith("-solved"):
        click.echo("Error: Directory is not marked as solved.", err=True)
        return
    new_name = dir_name.removesuffix("-solved")
    new_dir_path = rename_current_directory(new_name)
    set_cd_path(ctx, new_dir_path)

def rename_current_directory(new_name):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    new_dir_path = os.path.join(parent_dir, new_name)
    if os.path.exists(new_dir_path):
        click.echo(f"Error: A directory with the name '{new_name}' already exists.", err=True)
        return None
    try:
        os.rename(current_dir, new_dir_path)
        click.echo(f"Successfully renamed directory to '{new_name}'.")
        return new_dir_path
    except Exception as e:
        click.echo(f"Error renaming directory: {e}", err=True)
        return None
