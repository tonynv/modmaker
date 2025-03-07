"""
Tests for the commands module.
"""

from {{PROJECT_NAME}} import commands


def test_hello():
    """Test the hello function."""
    result = commands.hello("World")
    assert result == "Hello, World!"
    
    result = commands.hello("CLI")
    assert result == "Hello, CLI!"