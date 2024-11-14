import click

from cm.commands.add import add_command
from cm.commands.init import init_command
from cm.commands.solved import solved_command, unsolved_command

cli = click.Group()
cli.add_command(add_command)
cli.add_command(init_command)
cli.add_command(solved_command)
cli.add_command(unsolved_command)
