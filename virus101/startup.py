"""Startup utilities"""
import click
from utils import dots, print_title

STARTUP_ITEMS = ["kernel", "modules", "memory", "database"]
TITLE = "virus game"


async def startup() -> None:
    """Output at startup"""
    click.clear()
    click.secho("Starting up...", fg="green")
    for idx, item in enumerate(STARTUP_ITEMS, start=1):
        click.secho(f"[{idx}]  ", fg="blue", nl=False)
        click.secho(f"loading {item} .", nl=False)
        await dots(4)
        click.secho(" done!", fg="green")

    await print_title(TITLE)
