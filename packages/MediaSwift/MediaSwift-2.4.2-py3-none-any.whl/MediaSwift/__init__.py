# __init__.py
# -------------

"""
MEDIASWIFT - A PYTHON LIBRARY FOR MULTIMEDIA PROCESSING.
"""

import os

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

from .ffpe import ffpe
from .ffpr import ffpr
from .ffpl import ffpl

__all__ = ["ffpe", "ffpr", "ffpl", "version", "author"]

__version__ = "2.4.2"
__author__ = "ROHIT SINGH"


def author():
    """
    >>> RETURNS THE LIBRARY AUTHOR NAME.
    AUTHOR: ROHIT SINGH

    RETURN:
    -------
        >>> STR: THE LIBRARY AUTHOR NAME.

    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from MediaSwift import author

    INFO = author()
    print(INFO)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```
    >>> RETURN: NONE
    """
    author_name = Text("ROHIT SINGH 😄", style="bold magenta")
    console.print(
        Panel.fit(author_name, title="AUTHOR INFORMATION", border_style="green")
    )
    return " "


def version():
    """
    >>> RETURNS THE LIBRARY VERSION.

    RETURN:
    -------
        >>> STR: THE LIBRARY VERSION.

    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    from MediaSwift import version

    INFO = version()
    print(INFO)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ```

    >>> RETURN: NONE
    """
    version_info = Text("VERSION: " + __version__ + " ☑️", style="bold magenta")
    console.print(
        Panel.fit(version_info, title="VERSION INFORMATION", border_style="green")
    )
    return " "


def add_ffpe_to_path():
    """
    >>> ADD THE LIBRARY'S FFPE BINARY PATH TO THE SYSTEM PATH.
    """
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "..", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path


add_ffpe_to_path()
