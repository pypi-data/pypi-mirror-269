#!/usr/bin/env python3

import click
from click_default_group import DefaultGroup
from functools import wraps

from typing import Tuple, List, Union

from .utils import apple
from .utils.common import COLOR_PRESETS, resolve_fuzzy_color_preset_name


def load_quiet_option(func):
    """Decorator to add a quiet option to a command."""

    @click.option("--quiet", "-q", is_flag=True, help="Silence verbose stderr output.")
    @wraps(func)
    def wrapper(*args, **kwargs):
        quiet = kwargs.pop("quiet", False)
        ctx = click.get_current_context()
        ctx.ensure_object(dict)
        ctx.obj["quiet"] = quiet
        return func(*args, **kwargs)

    return wrapper


def parse_color_arg(colorarg, default_vals: Tuple[int] = (10, 10, 10)) -> Tuple[str]:

    if len(colorarg) == 0:
        cvals = default_vals
        verbose_echo(f"Default color: {cvals}")
    else:
        cname = resolve_fuzzy_color_preset_name(colorarg[0])
        # if only one argument: could be a preset name or the int for red in RGB
        if len(colorarg) == 1 and cname:
            cvals = COLOR_PRESETS[cname]
            verbose_echo(f"""Preset color "{cname}": {cvals}""")
        elif len(colorarg) <= 3:
            cvals = tuple(int(c) for c in (*colorarg, 0, 0)[:3])
            verbose_echo(f"RGB: {cvals}")
        else:
            raise ValueError(
                f"Expected `color` to be either a preset, or 1 to 3 RGB integers. Got: {colorarg}"
            )
    return cvals


def verbose_echo(message, **kwargs) -> None:
    """
    Custom echo function that checks quiet flag from context
    """
    ctx = click.get_current_context()
    if ctx.obj and ctx.obj.get("quiet") is not True:
        click.secho(message, err=True, **kwargs)


class DefaultRichGroup(DefaultGroup):
    """Make `click-default-group` work with `rick-click`."""


@click.version_option()
@click.group(cls=DefaultRichGroup, default="bg", default_if_no_args=True)
def cli():
    pass


@cli.command()
@load_quiet_option
@click.argument("color", nargs=-1, type=click.STRING)
def bg(color):
    """
    Change background color

    USAGE:
    # change background to black (default)
    $ tsty bg

    # change background to rgb of 100,200,0
    $ tsty bg 100 200

    # change background to "pink"
    $ tsty bg pink

    Pass in 1-3 int values for RGB, or color name like "red" or "lavender"

    default: 0,0,0 (i.e. black)
    """

    r, g, b = parse_color_arg(color, default_vals=(0, 0, 0))

    # if MacOS
    cmd = apple.get_color_change_command(r, g, b, "background color")
    verbose_echo(f"applescript:\n    {cmd}")
    apple.run_command(cmd)


@cli.command()
@load_quiet_option
@click.argument("color", nargs=-1, type=click.STRING)
def cursor(color):
    """
    Change cursor color

    USAGE:
    # change cursor to orange (default)
    $ tsty cursor
    """

    r, g, b = parse_color_arg(color, default_vals=(200, 130, 0))

    c = apple.get_color_change_command(r, g, b, "cursor color")
    verbose_echo(f"applescript:\n  {c}")
    apple.run_command(c)


@cli.command()
def list():
    """
    List commands and colors
    """
    click.echo(
        """
Commands:
  bg:       change background color (this is the default command)
  cursor:   change cursor color
  text:     change bold and normal text color
  reset:    reset terminal to sensible colors
""",
        err=True,
    )

    click.echo("Colors:", err=True)
    for c in COLOR_PRESETS.items():
        click.echo(f"  {c[0]}: {c[1]}", err=True)


@cli.command()
@load_quiet_option
@click.argument("color", nargs=-1, type=click.STRING)
@click.option("--bold", is_flag=True, default=False, help="Set color of bold text")
@click.option("--normal", is_flag=True, default=False, help="Set color of normal text")
def text(color, bold, normal):
    """
    Change text color (bold and/or normal)

    USAGE:
    # change bold and normal text to 255,255,255 (white is default)
    $ tsty text
    $ tsty text 255 255 255
    $ tsty text white

    # change just bold text to green
    $ tsty text green --bold

    # change just normal text to 100,200,255
    $ tsty text 100 200 --normal


    Pass in 1-3 int values for RGB, or color name like "red" or "lavender"

    default color: 255,255,255
    default: change both bold and normal text color
    """
    r, g, b = parse_color_arg(color, default_vals=(255, 255, 255))

    all_variations_when_nothing_flagged = bold is False and normal is False

    commands = []
    if bold is True or all_variations_when_nothing_flagged is True:
        commands.append(apple.get_color_change_command(r, g, b, "bold text color"))

    if normal is True or all_variations_when_nothing_flagged is True:
        commands.append(apple.get_color_change_command(r, g, b, "normal text color"))

    for c in commands:
        verbose_echo(f"applescript:\n  {c}")
        apple.run_command(c)


@cli.command()
@load_quiet_option
def reset():
    """
    Resets terminal colors to something sane:
    bg: offlback, text: offwhite, boldtext: white, cursor: orange
    """
    commands = []
    commands.append(apple.get_color_change_command(20, 20, 40, "background color"))
    commands.append(apple.get_color_change_command(255, 255, 255, "bold text color"))
    commands.append(apple.get_color_change_command(220, 220, 220, "normal text color"))
    commands.append(apple.get_color_change_command(200, 150, 0, "cursor color"))

    for c in commands:
        verbose_echo(f"applescript:\n  {c}")
        apple.run_command(c)


if __name__ == "__main__":
    cli()
