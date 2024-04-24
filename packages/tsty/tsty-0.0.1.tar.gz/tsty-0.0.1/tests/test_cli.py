import pytest
from click.testing import CliRunner
from tsty.cli import cli


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
    assert "(50, 0, 0)" in result.output, "Single int arg is used as red value, green and blue default to 0"


def test_cli_bg_one_int():
    runner = CliRunner()
    result = runner.invoke(cli, ["bg", "55", "66"])
    assert result.exit_code == 0
    assert "(55, 66, 0)" in result.output, "2 int arg is used as red and green, blue defaults to 0"

def test_cli_bg_three_ints():
    runner = CliRunner()
    result = runner.invoke(cli, ["bg", "11", "22", "33"])
    assert result.exit_code == 0
    assert "(11, 22, 33)" in result.output, "3 arguments are assumed to be 3 rgb values"
