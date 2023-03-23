import platform
from pathlib import Path

import pytest

# Default encoding is platform specific.
if platform.platform() == "Windows":
    CONSOLE_ENCODING = "cp437"
else:
    CONSOLE_ENCODING = "UTF-8"


def test_no_overrides(mock_sub):
    """With no overrides, there are still kwargs."""
    assert mock_sub.final_kwargs() == {
        "text": True,
        "encoding": CONSOLE_ENCODING,
        "errors": "backslashreplace",
    }


def test_explicit_no_overrides(mock_sub):
    """With explicitly no overrides, there are still kwargs."""
    assert mock_sub.final_kwargs(env=None) == {
        "env": {
            "VAR1": "Value 1",
            "PS1": "\nLine 2\n\nLine 4",
            "PWD": "/home/user/",
        },
        "text": True,
        "encoding": CONSOLE_ENCODING,
        "errors": "backslashreplace",
    }


def test_env_overrides(mock_sub):
    """If environmental overrides are provided, they supercede the default
    environment."""
    assert mock_sub.final_kwargs(env={"NEWVAR": "value", "VAR1": "New Value"}) == {
        "env": {
            "VAR1": "New Value",
            "PS1": "\nLine 2\n\nLine 4",
            "PWD": "/home/user/",
            "NEWVAR": "value",
        },
        "text": True,
        "encoding": CONSOLE_ENCODING,
        "errors": "backslashreplace",
    }


def test_cwd_provided(mock_sub):
    """If a cwd is provided, it is reflected in the environment."""
    cwd_override = "/my/current/path"
    assert mock_sub.final_kwargs(cwd=cwd_override) == {
        "text": True,
        "encoding": CONSOLE_ENCODING,
        "errors": "backslashreplace",
        "cwd": cwd_override,
    }


def test_non_str_cwd_provided(mock_sub):
    """If the cwd isn't a string, it's converted to string."""
    cwd_override = Path("/my/current/path")
    assert mock_sub.final_kwargs(cwd=cwd_override) == {
        "text": True,
        "encoding": CONSOLE_ENCODING,
        "errors": "backslashreplace",
        "cwd": str(cwd_override),
    }


@pytest.mark.parametrize(
    "in_kwargs, final_kwargs",
    [
        (
            {},
            {"text": True, "encoding": CONSOLE_ENCODING, "errors": "backslashreplace"},
        ),
        (
            {"text": True},
            {"text": True, "encoding": CONSOLE_ENCODING, "errors": "backslashreplace"},
        ),
        ({"text": False}, {"text": False}),
        ({"universal_newlines": False}, {"universal_newlines": False}),
        (
            {"universal_newlines": True},
            {
                "universal_newlines": True,
                "encoding": CONSOLE_ENCODING,
                "errors": "backslashreplace",
            },
        ),
        # Explicit encoding provided
        (
            {"encoding": "ibm850"},
            {"text": True, "encoding": "ibm850", "errors": "backslashreplace"},
        ),
        (
            {"text": True, "encoding": "ibm850"},
            {"text": True, "encoding": "ibm850", "errors": "backslashreplace"},
        ),
        (
            {"text": False, "encoding": "ibm850"},
            {"text": False, "encoding": "ibm850", "errors": "backslashreplace"},
        ),
        (
            {"universal_newlines": False, "encoding": "ibm850"},
            {
                "universal_newlines": False,
                "encoding": "ibm850",
                "errors": "backslashreplace",
            },
        ),
        (
            {"universal_newlines": True, "encoding": "ibm850"},
            {
                "universal_newlines": True,
                "encoding": "ibm850",
                "errors": "backslashreplace",
            },
        ),
    ],
)
def test_text_conversion(mock_sub, in_kwargs, final_kwargs):
    """Text/universal_newlines is correctly inserted/overridden, with encoding."""
    assert mock_sub.final_kwargs(**in_kwargs) == final_kwargs
