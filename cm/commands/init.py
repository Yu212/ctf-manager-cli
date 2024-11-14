import click

@click.command("init")
@click.option("-t", "--template", default="ipynb", help="Template files to use")
@click.option("-r", "--name-raw", is_flag=True, help="Use raw name")
@click.argument("name")
def init_command(template, name_raw, name):
    click.echo(f"init {template} {name_raw} {name}")
