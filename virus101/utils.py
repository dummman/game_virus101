"""Utility functions"""
import asyncio
import tkinter as tk
from tkinter import filedialog

import click


async def talk(msg: str, kwargs) -> None:
    """Shortcut function for virus talking"""
    click.secho(msg, **kwargs.value)
    await asyncio.sleep(2.0)


async def ask(msg: str, kwargs) -> bool:
    return click.confirm(click.style(msg, **kwargs.value), default=True)


async def prompt(msg: str, kwargs) -> str:
    return click.prompt(click.style(msg, **kwargs.value))


async def print_title(msg: str) -> None:
    click.echo("=" * len(msg))
    click.echo(msg)
    click.echo("=" * len(msg))


async def dots(number_dots: int, sleep_length: float = 0.2) -> None:
    """Display waiting dots"""
    for _ in range(number_dots):
        await asyncio.sleep(sleep_length)
        click.secho(".", nl=False)


async def file_prompt(start: str, title: str = "Bitte wähle eine Datei aus") -> str:
    """function for a file prompt in the foreground"""
    root = tk.Tk()
    root.withdraw()

    return filedialog.askopenfilename(initialdir=start, title=title)
