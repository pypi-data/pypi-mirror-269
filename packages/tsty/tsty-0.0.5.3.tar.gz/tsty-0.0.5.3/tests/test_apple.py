import pytest
from tsty.utils import apple


def test_get_color_change_command_returns_string():
    assert (
        type(apple.get_color_change_command(1, 2, 3)) is str
    ), "get command should return string representation of command to run"
