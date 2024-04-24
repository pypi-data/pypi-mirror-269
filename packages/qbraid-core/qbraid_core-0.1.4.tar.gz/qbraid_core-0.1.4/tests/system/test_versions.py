# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for qBraid core helper functions related to package versions.

"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from qbraid_core.exceptions import QbraidException
from qbraid_core.system.exceptions import InvalidVersionError, VersionNotFoundError
from qbraid_core.system.versions import (
    _simple_toml_version_extractor,
    extract_version,
    get_latest_package_version,
    get_local_package_version,
    is_valid_semantic_version,
)

try:
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import toml
    toml_available = True
except ImportError:
    toml_available = False


@pytest.mark.parametrize(
    "version_str, expected",
    [
        ("1.0.0", True),
        ("0.1.2", True),
        ("2.0.0-rc.1", True),
        ("1.0.0-alpha+001", True),
        ("1.2.3+meta-valid", True),
        ("+invalid", False),  # no major, minor or patch version
        ("-invalid", False),  # no major, minor or patch version
        ("1.0.0-", False),  # pre-release info cannot be empty if hyphen is present
        ("1.0.0+", False),  # build metadata cannot be empty if plus is present
        ("1.0.0+meta/valid", False),  # build metadata contains invalid characters
        ("1.0.0-alpha", True),
        ("1.1.2+meta-123", True),
        ("1.1.2+meta.123", True),
    ],
)
def test_is_valid_semantic_version(version_str, expected):
    """Test the is_valid_semantic_version function correctly parses version."""
    assert is_valid_semantic_version(version_str) == expected


def test_extract_version_from_package_json():
    """Test the extract_version function correctly extracts version from package.json."""
    mock_file_content = '{"version": "1.0.0-alpha.1"}'
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("json.load", return_value={"version": "1.0.0-alpha.1"}):
            assert extract_version("package.json", shorten_prerelease=True) == "1.0.0a1"


@pytest.mark.skipif(not toml_available, reason="Requires the toml or tomllib package")
def test_extract_version_from_pyproject_toml():
    """Test the extract_version function correctly extracts version from pyproject.toml."""
    mock_file_content = 'project = { version = "1.0.0-beta.2" }'
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("tomllib.load", return_value={"project": {"version": "1.0.0-beta.2"}}):
            assert extract_version("pyproject.toml") == "1.0.0-beta.2"


def test_unsupported_file_type():
    """Test the extract_version function raises ValueError for unsupported file type."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        extract_version("setup.cfg")


def test_file_not_found_error():
    """Test the extract_version function raises VersionNotFoundError when file is not found."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(VersionNotFoundError, match="Unable to find or read"):
            extract_version("nonexistent.json")


def test_missing_version_key_error():
    with patch("builtins.open", mock_open(read_data="{}")):
        with patch("json.load", return_value={}):
            with pytest.raises(VersionNotFoundError, match="Unable to find or read"):
                extract_version("package.json")


def test_io_error_on_file_read():
    """Test the extract_version function raises VersionNotFoundError when file cannot be read."""
    with patch("builtins.open", side_effect=IOError):
        with pytest.raises(VersionNotFoundError, match="Unable to find or read"):
            extract_version("package.json")


@pytest.mark.skipif(not toml_available, reason="Requires the toml or tomllib package")
def test_invalid_version_error():
    """Test the extract_version function raises InvalidVersionError for invalid semantic version."""
    mock_file_content = 'project = { version = "helloWorld" }'
    with patch("builtins.open", mock_open(read_data=mock_file_content)):
        with patch("tomllib.load", return_value={"project": {"version": "helloWorld"}}):
            with pytest.raises(InvalidVersionError, match="Invalid semantic version"):
                extract_version("pyproject.toml", check=True)


def test_simple_toml_version_extractor_success():
    """Test the _simple_toml_version_extractor function successfully extracts version."""
    mock_toml_content = '[project]\nversion = "1.2.3"\n'
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        version = _simple_toml_version_extractor("pyproject.toml")
        assert version == "1.2.3", "The version should be extracted successfully."


def test_simple_toml_version_extractor_no_version_key():
    """Test the _simple_toml_version_extractor function raises ValueError when version key is not found."""
    mock_toml_content = '[project]\nname = "example"\n'
    with patch("builtins.open", mock_open(read_data=mock_toml_content)):
        with pytest.raises(ValueError, match="Version key not found in the TOML content."):
            _simple_toml_version_extractor("pyproject.toml")


def test_simple_toml_version_extractor_file_not_found():
    """Test the _simple_toml_version_extractor function raises VersionNotFoundError when file is not found."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(VersionNotFoundError, match="The specified TOML file does not exist."):
            _simple_toml_version_extractor("pyproject.toml")


def test_simple_toml_version_extractor_io_error():
    """Test the _simple_toml_version_extractor function raises VersionNotFoundError when file cannot be read."""
    with patch("builtins.open", side_effect=IOError):
        with pytest.raises(
            VersionNotFoundError, match="An error occurred while reading the TOML file."
        ):
            _simple_toml_version_extractor("pyproject.toml")


def test_get_latest_version_raises():
    """Test the _get_latest_version function when an error occurs."""
    with pytest.raises(VersionNotFoundError):
        get_latest_package_version("nonexistent_package")


@pytest.mark.parametrize(
    "package,python_path", [("not_a_package", None), ("not_a_package", sys.executable)]
)
def test_get_local_version_raises_for_bad_package(package, python_path):
    """Test the _get_local_version function when an error occurs."""
    with pytest.raises(QbraidException) as exc_info:
        get_local_package_version(package, python_path=python_path)
    assert f"{package} not found in the current environment." in str(exc_info)


def test_get_local_version_raises_for_():
    """Test the _get_local_version function when an error occurs."""
    package = "pytest"  # valid package guaranteed to be installed
    python_path = "/bad/python/path"  # invalid python path
    with pytest.raises(QbraidException) as exc_info:
        get_local_package_version(package, python_path=python_path)
    assert f"Python executable not found at {python_path}." in str(exc_info)


@pytest.mark.parametrize("python_path", [None, Path(sys.executable), sys.executable])
def test_get_local_package_version_alt_python(python_path):
    """Test the get_latest_package_version function with an alternative Python path."""
    python_path = Path(sys.executable)
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(stdout="2.31.0\n")
        assert get_local_package_version("requests", python_path=python_path) == "2.31.0"
