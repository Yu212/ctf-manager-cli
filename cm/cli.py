import click

from cm.commands.add import add_command
from cm.commands.init import init_command
from cm.commands.solved import solved_command, unsolved_command


@click.group()
@click.pass_context
@click.option("--out-cd-path", help="Output cd path")
def cli(ctx, out_cd_path):
    ctx.ensure_object(dict)["out_cd_path"] = out_cd_path

cli.add_command(add_command)
cli.add_command(init_command)
cli.add_command(solved_command)
cli.add_command(unsolved_command)
