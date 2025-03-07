"""
Tests for the CLI.
"""

from click.testing import CliRunner

from {{PROJECT_NAME}}.cli import cli


def test_cli_version():
    """Test the CLI version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_greet():
    """Test the greet command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["greet", "--name", "Tester"])
    assert result.exit_code == 0
    assert "Hello, Tester" in result.output