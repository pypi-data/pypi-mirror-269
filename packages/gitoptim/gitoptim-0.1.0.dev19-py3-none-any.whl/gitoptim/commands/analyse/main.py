import typer

from gitoptim.utils.cli import console, should_callback_execute

from ...utils.tag import TagFactory
from .logs import command as logs

app = typer.Typer(rich_markup_mode="rich")


# pylint: disable=unused-argument
def teardown(*args, **kwargs):
    console.print(TagFactory.create_end_tag())


@app.callback(result_callback=teardown)
def main():
    """
    Analyse code or Gitlab job logs.
    """

    if not should_callback_execute():
        return

    console.print(TagFactory.create_start_tag())


app.command(name="logs")(logs)
