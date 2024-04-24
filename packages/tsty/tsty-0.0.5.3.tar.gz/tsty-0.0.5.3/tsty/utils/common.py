import re
from typing import Union, Tuple


COLOR_PRESETS = {
    "blue": (0, 0, 100),
    "cyan": (0, 90, 90),
    "green": (0, 100, 0),
    "lavender": (80, 50, 95),
    "magenta": (80, 10, 80),
    "navy": (5, 5, 55),
    "orange": (150, 80, 0),
    "pink": (150, 80, 80),
    "slate": (80, 90, 105),
    "red": (100, 0, 0),
    "yellow": (130, 130, 0),
    # secondary colors
    "black": (0, 0, 0),
    "brown": (
        50,
        30,
        0,
    ),
    "gray": (50, 50, 50),
    "purple": (60, 0, 60),
    "seagreen": (30, 120, 60),
    "white": (255, 255, 255),
}


def resolve_fuzzy_color_preset_name(textval: str) -> Union[str, None]:
    """
    Allow users to pick colors by typing in first few letters, e.g. "b" resolves to "blue"
    """

    if textval.isdigit():
        return None

    preset_names = COLOR_PRESETS.keys()

    txt = textval.lower()
    if txt in preset_names:
        return txt
    else:
        # handle abbreviations, e.g. "b" should be blue
        return next((n for n in preset_names if re.match(txt, n)), None)
