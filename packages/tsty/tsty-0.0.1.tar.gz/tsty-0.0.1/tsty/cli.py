#!/usr/bin/env python3

import click
from click_default_group import DefaultGroup
from functools import wraps

import re
import subprocess
from typing import TextIO, List, Union

from tsty.utils import apple


COLOR_PRESETS = {
    'blue': (0, 0, 80),
    'green': (0, 80, 0),
    'red': (80, 0, 0),
    'pink': (150, 80, 80),
    'lavender': (80, 50, 95),
    'purple': (50, 0, 50),
    'gray': (50, 50, 50),
    'black': (0, 0, 0),
    'white': (225, 225, 225),
}

def load_quiet_option(func):
    """Decorator to add a quiet option to a command."""
    @click.option('--quiet', '-q', is_flag=True, help="Silence verbose stderr output.")
    @wraps(func)
    def wrapper(*args, **kwargs):
        quiet = kwargs.pop('quiet', False)
        ctx = click.get_current_context()
        ctx.ensure_object(dict)
        ctx.obj['quiet'] = quiet
        return func(*args, **kwargs)
    return wrapper


def resolve_potential_color_preset_name(textval:str) -> Union[str, None]:
    if textval.isdigit():
        return None

    preset_names = COLOR_PRESETS.keys()

    txt = textval.lower()
    if txt in preset_names:
        return txt
    else:
        # handle abbreviations, e.g. "b" should be blue
        return next((n for n in preset_names if re.match(txt, n)), None)



def verbose_echo(message, **kwargs) -> None:
    """
    Custom echo function that checks quiet flag from context
    """
    ctx = click.get_current_context()
    if ctx.obj and ctx.obj.get('quiet') is not True:
         click.secho(message, err=True, **kwargs)


class DefaultRichGroup(DefaultGroup):
    """Make `click-default-group` work with `rick-click`."""

@click.version_option()
@click.group(cls=DefaultRichGroup, default="bg", default_if_no_args=True)
def cli():
    pass



@cli.command()
@load_quiet_option
@click.argument(
    "color",
    nargs=-1,
    type=click.STRING
)
def bg(color):
    """
    pass in r g b values
    """


    if len(color) == 0:
        cvals = (0, 0, 0)
        verbose_echo(f"Defaulting to black: {cvals}")
    else:
        cname = resolve_potential_color_preset_name(color[0])
        # if only one argument: could be a preset name or the int for red in RGB
        if len(color) == 1 and cname:
            cvals = COLOR_PRESETS[cname]
            verbose_echo(f"""Preset color "{cname}": {cvals}""")
        elif len(color) <= 3:
            cvals = tuple(int(c) for c in (*color, 0, 0)[:3])
            verbose_echo(f"RGB: {cvals}")
        else:
            raise ValueError(f"Expected `color` to be either a preset, or 1 to 3 RGB integers. Got: {color}")

    r, g, b = cvals

    # if MacOS
    color_cmd = apple.get_color_change_command(r, g, b)
    verbose_echo(f"applescript:\n    {color_cmd}")
    apple.run_command(color_cmd)

if __name__ == "__main__":
    cli()
