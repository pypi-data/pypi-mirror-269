import pytest
from click.testing import CliRunner
from tsty.cli import cli


def pytest_sessionfinish(session, exitstatus):
    """clean up the terminal colors"""
    CliRunner().invoke(
        cli,
        [
            "reset",
        ],
    )


def test_help_option():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--help " in result.output


def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_cli_bg_one_int():
    runner = CliRunner()
    result = runner.invoke(cli, ["bg", "50"])
    assert result.exit_code == 0
    assert (
        "(50, 0, 0)" in result.output
    ), "Single int arg is used as red value, green and blue default to 0"


def test_cli_bg_one_int():
    runner = CliRunner()
    result = runner.invoke(cli, ["bg", "55", "66"])
    assert result.exit_code == 0
    assert (
        "(55, 66, 0)" in result.output
    ), "2 int arg is used as red and green, blue defaults to 0"


def test_cli_bg_three_ints():
    runner = CliRunner()
    result = runner.invoke(cli, ["bg", "11", "22", "33"])
    assert result.exit_code == 0
    assert "(11, 22, 33)" in result.output, "3 arguments are assumed to be 3 rgb values"


##############################################
# cursor
##############################################


def test_cli_cursor_default():
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "cursor",
        ],
    )
    assert result.exit_code == 0
    assert (
        f"set cursor color of window 1" in result.output
    ), f"Modfies the 'cursor color' attribute"


def test_cli_cursor_white():
    runner = CliRunner()

    result = runner.invoke(cli, ["cursor", "white"])
    assert result.exit_code == 0
    assert "(255, 255, 255)" in result.output, "Make sure cursor can accept a color"

    assert (
        "set cursor color of window 1 to {65535, 65535, 65535}" in result.output
    ), f"sets the 'cursor color' attribute to white"


##############################################
# text
##############################################


def test_cli_text_no_args_default():
    runner = CliRunner()

    variations = (
        "bold",
        "normal",
    )

    result = runner.invoke(
        cli,
        [
            "text",
        ],
    )
    assert result.exit_code == 0
    assert "255, 255, 255" in result.output, "255 is default text color"

    for v in variations:
        assert (
            f"set {v} text color of window 1 to {{65535, 65535, 65535}}"
            in result.output
        ), f"When no variation flagged, {v} text is included by default"


def test_cli_text_one_flag_invalidates_others():
    runner = CliRunner()
    variations = (
        "bold",
        "normal",
    )

    for tested_flag in variations:
        result = runner.invoke(cli, ["text", f"--{tested_flag}"])

        for v in variations:
            if v == tested_flag:
                assert (
                    f"set {tested_flag} text color" in result.output
                ), f"{tested_flag} is flagged; {v} text is altered"
            else:
                assert (
                    f"set {v} text color" not in result.output
                ), f"{tested_flag} flag is flagged; by default {v} text is ignored"


def test_cli_text_one_int():
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "text",
            "55",
        ],
    )
    assert result.exit_code == 0
    assert "(55, 0, 0)" in result.output, "1 int arg is used as red"

    assert (
        "set bold text color of window 1" in result.output
    ), "default flag includes bold text"

    assert (
        "set normal text color of window 1" in result.output
    ), "default flag includes normal text"
