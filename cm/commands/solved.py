import click

@click.command("solved")
def solved_command():
    click.echo("solved")

@click.command("unsolved")
def unsolved_command():
    click.echo("unsolved")
