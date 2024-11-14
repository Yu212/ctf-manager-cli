import click

@click.command("add")
@click.argument("source")
def add_command(source):
    click.echo(f"add {source}")
