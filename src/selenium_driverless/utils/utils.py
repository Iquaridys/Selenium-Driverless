# from https://github.com/ultrafunkamsterdam/undetected-chromedriver/blob/1c704a71cf4f29181a59ecf19ddff32f1b4fbfc0/undetected_chromedriver/__init__.py#L844
# edited by kaliiiiiiiiii | Aurin Aegerter

import sys
import typing
import os
import time

import socket
import selenium
import selenium_driverless
from contextlib import closing
import aiofiles

IS_POSIX = sys.platform.startswith(("darwin", "cygwin", "linux", "linux2"))
T_JSON_DICT = typing.Dict[str, typing.Any]


def find_chrome_executable():
    """
    Finds the Chrome, Chrome beta, Chrome canary, Chromium executable

    Returns
    -------
    executable_path :  str
        the full file path to found executable

    """
    candidates = set()
    if IS_POSIX:
        for item in os.environ.get("PATH").split(os.pathsep):
            for subitem in (
                    "google-chrome",
                    "chromium",
                    "chromium-browser",
                    "chrome",
                    "google-chrome-stable",
            ):
                candidates.add(os.sep.join((item, subitem)))
        if "darwin" in sys.platform:
            candidates.update(
                [
                    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                    "/Applications/Chromium.app/Contents/MacOS/Chromium",
                ]
            )
    else:
        for item in map(
                os.environ.get,
                ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA", "PROGRAMW6432"),
        ):
            if item is not None:
                for subitem in (
                        "Google/Chrome/Application",
                        "Google/Chrome Beta/Application",
                        "Google/Chrome Canary/Application",
                ):
                    candidates.add(os.sep.join((item, subitem, "chrome.exe")))
    for candidate in candidates:
        if os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return os.path.normpath(candidate)


def sel_driverless_path():
    return os.path.dirname(selenium_driverless.__file__) + "/"


def sel_path():
    return os.path.dirname(selenium.__file__) + "/"


async def read(filename: str, encoding: str = "utf-8", sel_root: bool = True):
    if sel_root:
        path = sel_driverless_path() + filename
    else:
        path = filename
    async with aiofiles.open(path, encoding=encoding) as f:
        return await f.read()


async def write(filename: str, content: str, encoding: str = "utf-8", sel_root: bool = True):
    if sel_root:
        path = sel_driverless_path() + filename
    else:
        path = filename
    async with aiofiles.open(path, "w+", encoding=encoding) as f:
        return await f.write(content)


def random_port(host: str = None):
    if not host:
        host = ''
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def check_timeout(start_monotonic: float, timeout: float):
    if (time.monotonic() - start_monotonic) > timeout:
        raise TimeoutError(f"driver.quit took longer than timeout: {timeout}")


async def is_first_run():
    res = await read("files/is_first_run")
    return res == "true"


def reset_all():
    import asyncio
    async def _reset_all():
        await write("files/is_first_run", "true")
        await write("files/useragent", "")

    asyncio.run(_reset_all())
    print("resetting all")
