"""Test basic project setup."""

import drawing_lib


def test_version() -> None:
    """Test that version is available."""
    assert hasattr(drawing_lib, "__version__")
    assert drawing_lib.__version__ == "0.1.0"