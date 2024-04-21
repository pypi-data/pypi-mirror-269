# SPDX-FileCopyrightText: 2024-present MtkN1 <51289448+MtkN1@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
try:
    from setuptools_scm import get_version

    __version__ = get_version()
except Exception:
    from importlib.metadata import version

    __version__ = version(__package__)
