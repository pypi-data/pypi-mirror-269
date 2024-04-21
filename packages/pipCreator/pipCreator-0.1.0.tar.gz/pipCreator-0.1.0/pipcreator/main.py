import click

from pipcreator.writer import pip_creator
from pipcreator.convert import run_setup_command_convert
from pipcreator.upload import run_setup_command_upload
from pipcreator.guide import guide_learn
from pipcreator.createtest import test_folder

@click.group()
def cli():
    pass

@click.command()
@click.argument('directory')
def create(directory):
    directory = str(directory)
    pip_creator()


@click.command()
def create_test():
    test_folder()

@click.command()
def convert():
    run_setup_command_convert()

@click.command()
def upload():
    run_setup_command_upload()

@click.command()
def guide():
    guide_learn()

cli.add_command(create)
cli.add_command(convert)
cli.add_command(upload)
cli.add_command(guide)
cli.add_command(create_test)