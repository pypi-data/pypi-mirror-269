# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Script for getting/bumping the next pre-release version.

"""

import pathlib

from packaging.version import Version, parse

from qbraid_core.system import extract_version, get_latest_package_version

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.resolve()
PYPROJECT_TOML_PATH = PROJECT_ROOT / "pyproject.toml"

PACKAGE_NAME = "qbraid_core"


class PreReleaseVersionError(Exception):
    """Class for exceptions raised while stamping pre-release version."""


def get_bumped_version(latest: str, local: str) -> str:
    """Compare latest and local versions and return the bumped version."""
    latest_version = parse(latest)
    local_version = parse(local)

    def bump_prerelease(version: Version) -> str:
        if version.pre:
            pre_type, pre_num = version.pre[0], version.pre[1]
            return f"{version.base_version}-{pre_type}.{pre_num + 1}"
        return f"{version.base_version}-a.0"

    if local_version.base_version > latest_version.base_version:
        return f"{local_version.base_version}-a.0"
    if local_version.base_version == latest_version.base_version:
        if latest_version.is_prerelease:
            if local_version.is_prerelease:
                if local_version.pre[0] == latest_version.pre[0]:
                    if local_version.pre[1] > latest_version.pre[1]:
                        raise PreReleaseVersionError(
                            "Local version prerelease is newer than latest version."
                        )
                    return bump_prerelease(latest_version)
                if local_version.pre[0] < latest_version.pre[0]:
                    return bump_prerelease(latest_version)
                return f"{local_version.base_version}-{local_version.pre[0]}.0"
            raise PreReleaseVersionError("Latest version is prerelease but local version is not.")
        if local_version.is_prerelease:
            return f"{local_version.base_version}-{local_version.pre[0]}.0"
        if local_version == latest_version:
            return f"{local_version.base_version}-a.0"
        raise PreReleaseVersionError(
            "Local version base is equal to latest, but no clear upgrade path found."
        )
    raise PreReleaseVersionError("Latest version base is greater than local, cannot bump.")


if __name__ == "__main__":

    if not PYPROJECT_TOML_PATH.exists():
        raise FileNotFoundError("pyproject.toml not found")

    v_local = extract_version(PYPROJECT_TOML_PATH, shorten_prerelease=True)
    v_latest = get_latest_package_version(PACKAGE_NAME, prerelease=True)
    v_prerelease = get_bumped_version(v_latest, v_local)
    print(v_prerelease)
