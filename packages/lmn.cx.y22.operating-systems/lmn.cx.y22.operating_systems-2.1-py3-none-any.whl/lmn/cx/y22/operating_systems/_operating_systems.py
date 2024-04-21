# SPDX-FileCopyrightText: 2024 Alex Lemna
# SPDX-License-Identifier: 0BSD OR MIT OR Apache-2.0
#
# This source code is available to you under your choice of any
# of the following licenses:
#   - The BSD Zero Clause License (or `0BSD`)
#   - The MIT License (or `MIT`)
#   - The Apache License 2.0 (or `Apache-2.0`)
# For more information, see the COPYING file or the LICENSES
# directory at the root of this repository.
#

import importlib.metadata
from dataclasses import dataclass
from enum import Enum
from typing import Any, Final

__all__ = ["determine_os", "OperatingSystem", "OS"]
try:
    __version__ = importlib.metadata.version("lmn.cx.y22.operating_systems")
except importlib.metadata.PackageNotFoundError:
    __version__ = "UNKNOWN"


@dataclass(frozen=True, init=False)
class OperatingSystem:
    os_name: str
    unix_like: bool
    xdg: bool

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if (
            "xdg" not in kwds.keys()
            and "unix_like" in kwds.keys()
            and kwds["unix_like"] is True
        ):
            kwds["xdg"] = True

        return self.__init__(*args, **kwds)

    def __init__(
        self,
        name_or_os: "str | OperatingSystem",
        unix_like: bool = False,
        xdg: bool = False,
    ) -> None:
        # if we're being initialized with an argument that is
        # already an OperatingSystem, then we should just make
        # ourselves identical to it. After all, int(int(x))
        # should be the same as int(x).
        if isinstance(name_or_os, OperatingSystem):
            _os = name_or_os
            object.__setattr__(self, "os_name", _os.os_name)
            object.__setattr__(self, "unix_like", _os.unix_like)
            object.__setattr__(self, "xdg", _os.xdg)

        # Otherwise, we can assume the first argument we're
        # being initialized with is a string.
        else:
            os_name = name_or_os
            object.__setattr__(self, "os_name", os_name)
            object.__setattr__(self, "unix_like", unix_like)
            object.__setattr__(self, "xdg", xdg)


class OS(OperatingSystem, Enum):
    ANDROID: Final = OperatingSystem("Android")
    FREEBSD: Final = OperatingSystem("FreeBSD", unix_like=True)
    iOS: Final = OperatingSystem("iOS")
    LINUX: Final = OperatingSystem("Linux", unix_like=True)
    MAC: Final = OperatingSystem("macOS", unix_like=True, xdg=False)
    NETBSD: Final = OperatingSystem("NetBSD", unix_like=True)
    OPENBSD: Final = OperatingSystem("OpenBSD", unix_like=True)
    UNKNOWN: Final = OperatingSystem("UNKNOWN")
    WINDOWS: Final = OperatingSystem("Windows")


def determine_os() -> OS:
    # fmt: off
    try:
        from sys import getandroidapilevel  # type: ignore
        return OS.ANDROID
    except ImportError:
        import sys
    # fmt: on

    if sys.platform.startswith("freebsd"):
        return OS.FREEBSD

    # requires Python 3.13
    #   see: https://peps.python.org/pep-0730/#platform-identification
    if sys.platform == "ios":
        return OS.iOS

    if sys.platform == "linux":
        return OS.LINUX

    if sys.platform == "darwin":
        return OS.MAC

    if sys.platform.startswith("netbsd"):
        return OS.NETBSD

    if sys.platform.startswith("openbsd"):
        return OS.OPENBSD

    if sys.platform == "win32":
        return OS.WINDOWS

    return OS.UNKNOWN
