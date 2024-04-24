# ffpl.py
# ---------

import gc
import os
from rich.panel import Panel
from rich.console import Console
import subprocess
from functools import lru_cache
import time
from pathlib import Path
from rich.traceback import install

install(show_locals=True)
console = Console()


def clear_console():
    # CLEAR CONSOLE SCREEN.
    """
    >>> CLEAR SCREEN FUNCTION.
    """
    if os.name == "nt":
        _ = os.system("cls")  # FOR WINDOWS
    else:
        _ = os.system("clear")  # FOR LINUX/MACOS


class ffpl:
    """
    >>> CLASS FOR INTERFACING TO PLAY MULTIMEDIA FILES.

    ATTRIBUTES
    ----------
    >>> ⇨ FFPL_PATH : STR
        >>> PATH TO THE FFPL EXECUTABLE.

    METHODS
    -------
    >>> ⇨ PLAY(MEDIA_FILE)
        >>> PLAY MULTIMEDIA FILE.
    >>> EXAMPLE:

    ```python
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >>> from MediaSwift import ffpl
    >>> PLAY = ffpl()

        # INCREASE VOLUME BY 5 DB(DECIBEL)
    >>> MEDIA_FILE  = r"PATH_TO_MEDIA_FILE"

    >>> PLAY.play(MEDIA_FILE , volume = 5, noborder=True)
    >>> PLAY.play_multiple(MEDIA_FILE, volume=5, noborder=True)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    >>> PLAY MULTIPLE MEDIA FILE USING play_multiple

    ```
    >>> RETURNS: NONE
    """

    def __init__(self):
        """
        >>> INITIALIZE THE FFPL INSTANCE.
        >>> SETS THE DEFAULT PATH TO THE FFPL EXECUTABLE.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> PLAY = ffpl()
        >>> MEDIA_FILE = r"PATH_TO_MEDIA_FILE"
        >>> PLAY.play(MEDIA_FILE )

        >>> PLAY.play(MEDIA_FILE , noborder=True)
        >>> PLAY.play_multiple(media_file, volume=5, noborder=True)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURN: NONE
        """
        self.ffplay_path = Path(__file__).resolve().parent / "bin" / "ffpl.exe"

    @lru_cache(maxsize=None)  # SETTING MAXSIZE TO NONE MEANS AN UNBOUNDED CACHE
    def play(self, media_file, volume=0, noborder=False):
        """
        >>> PLAY MULTIMEDIA FILE USING FFPL WITH SPECIFIED VIDEO FILTERS.

        ⇨ PARAMETER'S
        ------------
        >>> MEDIA_FILE : STR
           >>> PATH TO THE MULTIMEDIA FILE TO BE PLAYED.

        >>> EXAMPLE:

        ```python
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        >>> from MediaSwift import ffpl

        >>> PLAY = ffpl()
        >>> MEDIA_FILE  = r"PATH_TO_MEDIA_FILE"

        # INCREASE VOLUME BY 5 DB(DECIBEL)
        >>> PLAY.play(MEDIA_FILE ,volume=5)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```
        >>> RETURNS: NONE

        """
        if not Path(media_file).exists():
            clear_console()
            console.print(
                Panel.fit(
                    f"ERROR: THE FILE PATH [bold green]{media_file.upper()}[/bold green] DOES NOT EXIST.",
                    style="bold red",
                )
            )
            return

        if not Path(media_file).is_file():
            clear_console()
            console.print(
                Panel.fit(
                    f"ERROR: [bold green]{media_file.upper()}[/bold green] IS NOT A FILE PATH.",
                    style="bold red",
                )
            )
            return

        # MODIFY THE COMMAND TO INCLUDE THE OPTIONS FOR SETTING.
        command = [
            str(self.ffplay_path),
            "-hide_banner",
            "-window_title",
            "MEDIA PLAYER",
            "-x",
            "1480",
            "-vf",
            "hqdn3d,unsharp",
            "-loglevel",
            "panic",  # ADJUSTED LOG LEVEL HERE
            "-af",
            f"volume={volume}dB",
        ]

        if noborder:
            command.append("-noborder")

        command.append(str(media_file))

        clear_console()
        console.print(
            Panel.fit("MEDIA PLAYER. NOW PLAYING :Musical_Notes:", style="bold green")
        )

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            console.print(
                f"AN ERROR OCCURRED WHILE PLAYING THE MEDIA FILE: {e}", style="bold red"
            )
        except Exception as e:
            console.print(f"AN UNEXPECTED ERROR OCCURRED: {e}", style="bold red")
        finally:
            clear_console()
            console.print(
                Panel.fit("MEDIA PLAYER EXITED.. :Waving_Hand:", style="bold yellow")
            )
            time.sleep(2)
            gc.collect()
            clear_console()
            return " "

    @lru_cache(maxsize=None)
    def play_multiple(self, media_files, volume=0, noborder=False):
        """
        >>> PLAYS MULTIPLE MULTIMEDIA FILES USING FFPL WITH SPECIFIED OPTIONS.

        PARAMETERS:
        ----------------
        >>> MEDIA_FILES (LIST OF STR): LIST OF PATHS TO THE MULTIMEDIA FILES TO BE PLAYED.
        >>> VOLUME (INT, OPTIONAL): VOLUME LEVEL IN DB (DECIBEL). DEFAULT IS 0.
        >>> NOBORDER (BOOL, OPTIONAL): WHETHER TO HIDE BORDER DURING PLAYBACK. DEFAULT IS FALSE.

        >>> EXAMPLE:

        ```PYTHON
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        from MediaSwift import ffpl

        PLAY = FFPL()
        MEDIA_FILES = [
            R"PATH_TO_MEDIA_FILE_1",
            R"PATH_TO_MEDIA_FILE_2",
            R"PATH_TO_MEDIA_FILE_3",
        ]
        PLAY.PLAY_MULTIPLE(MEDIA_FILES, VOLUME=5, NOBORDER=TRUE)
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ```

        >>> RETURNS: NONE
        """

        try:
            for media_file in media_files:
                process = subprocess.Popen(
                    [
                        str(self.ffplay_path),
                        "-hide_banner",
                        "-window_title",
                        "MEDIA PLAYER",
                        "-x",
                        "1480",
                        "-vf",
                        "hqdn3d,unsharp",
                        "-loglevel",
                        "panic",
                        "-af",
                        f"volume={volume}dB",
                        "-autoexit",
                    ]
                    + (["-noborder"] if noborder else [])
                    + [str(media_file)]
                )
                os.system("cls" if os.name == "nt" else "clear")
                console.print(
                    Panel.fit(
                        "MEDIA PLAYER. NOW PLAYING :Musical_Notes:", style="bold green"
                    )
                )
                process.wait()
                console.print(
                    Panel.fit(
                        f"FINISHED PLAYING ({media_file.upper()})", style="bold red"
                    )
                )
                time.sleep(2)
                os.system("cls" if os.name == "nt" else "clear")
        finally:
            console.print(
                Panel.fit("MEDIA PLAYER EXITED.. :Waving_Hand:", style="bold yellow")
            )
            time.sleep(2)
            clear_console()
            gc.collect()
            return " "
