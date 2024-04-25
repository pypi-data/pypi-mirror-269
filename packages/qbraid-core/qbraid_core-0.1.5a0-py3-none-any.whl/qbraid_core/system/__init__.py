# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module serving qBraid system information.

.. currentmodule:: qbraid_core.system

Classes
--------

.. autosummary::
   :toctree: ../stubs/

   FileManager

Functions
----------

.. autosummary::
   :toctree: ../stubs/

   extract_version
   is_exe
   is_valid_python
   is_valid_semantic_version
   get_python_version_from_cfg
   get_python_version_from_exe
   get_venv_site_packages_path
   get_active_site_packages_path
   get_active_python_path
   get_local_package_path
   get_local_package_version
   get_latest_package_version
   python_paths_equivalent
   add_config_path_to_site_packages
   remove_config_path_from_site_packages
   replace_str
   echo_log


Exceptions
------------

.. autosummary::
   :toctree: ../stubs/

   InvalidVersionError
   QbraidSystemError
   UnknownFileSystemObjectError
   VersionNotFoundError

"""
from .exceptions import (
    InvalidVersionError,
    QbraidSystemError,
    UnknownFileSystemObjectError,
    VersionNotFoundError,
)
from .executables import (
    get_active_python_path,
    get_python_version_from_cfg,
    get_python_version_from_exe,
    is_exe,
    is_valid_python,
    python_paths_equivalent,
)
from .generic import echo_log, replace_str
from .packages import (
    add_config_path_to_site_packages,
    get_active_site_packages_path,
    get_local_package_path,
    get_venv_site_packages_path,
    remove_config_path_from_site_packages,
)
from .threader import FileManager
from .versions import (
    extract_version,
    get_latest_package_version,
    get_local_package_version,
    is_valid_semantic_version,
)
