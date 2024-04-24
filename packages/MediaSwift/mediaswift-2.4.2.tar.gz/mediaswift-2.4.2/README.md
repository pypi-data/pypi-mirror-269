## `MediaSwift` ⇨ 🚀 EMPOWERING PYTHON WITH ADVANCED MULTIMEDIA OPERATION'S.

[![License](https://img.shields.io/badge/LICENSE-MIT-blue?style=flat-square&logo=gnu%20bash)](https://github.com/ROHIT-SINGH-1/PYTHON-MEDIASWIFT/blob/main/LICENSE)

#### ⇨ `MediaSwift` : A POWERFUL PYTHON LIBRARY FOR SEAMLESS MULTIMEDIA OPERATIONS , `MediaSwift` SIMPLIFIES COMPLEX TASKS, MAKING IT EASY TO INTEGRATE AND ENHANCE YOUR MULTIMEDIA APPLICATIONS. DIVE INTO THE FUTURE OF MEDIA HANDLING WITH `MediaSwift` YOUR GO-TO LIBRARY FOR 2024 .

**KEY FEATURES :**

- **EFFORTLESS FILE CONVERSION .**
- **SEAMLESS MULTIMEDIA PLAYBACK .**
- **PROVIDING INFORMATION `MediaSwift` ALSO OFFERS DETAILED MULTIMEDIA INFORMATION RETRIEVAL .**

### EXPLORE THE CAPABILITIES OF `MediaSwift` AND ELEVATE YOUR PYTHON MULTIMEDIA PROJECTS WITH SIMPLICITY AND EFFICIENCY.

- ## SUPPORTED VIDEO CODEC'S :

  `h264`, `libx264`, `mpeg4`, `vp9`, `av1`, `hevc`, `mjpeg`, `H.265 / HEVC`, `VP8`, `VP9`, `AV1`, `VC1`, `MPEG1`, `MPEG2`, `H.263`, `Theora`, `MJPEG`, `MPEG-3`, `MPEG-4` **. . .**

- ## SUPPORTED AUDIO CODEC'S :

  `aac`, `mp3`, `opus`, `vorbis`, `pcm`, `alac`, `flac`, `wv`, `ape`, `mka`, `opus`, `ac3`, `eac3`, `alac` **. . .**

- ## SUPPORTED FILE EXTENSION'S :
  **VIDEO FORMATS :** `.mp4`, `.avi`, `.mkv`, `.webm`, `.mov`, `.wmv`, `.webm`, `.flv`, `.mov`, `.wmv`, `.hevc`, `.prores`, `.dv` **. . .**

**AUDIO FORMATS :** `.mp3`, `.aac`, `.ogg`, `.wav`, `.flac`, `.flac`, `.m4a`, `.ogg`, `.wv`, `.ape`, `.mka`, `.opus`, `mpc`, `.tak`, `.alac` **. . .**

- ## SUPPORTED HARDWARE ACCELERATION :
  **HARDWARE ACCELERATION :** `cuda`, `dxva2`, `qsv`, `d3d11va` **. . .**

## ❗IMPORTANT NOTE:

- **THEY ALSO SUPPORT HARDWARE ACCELERATION FOR MEDIA FILE CONVERTION .**
- **SUPPORT DOLBY DIGITAL PLUS AND DOLBY DIGITAL AUDIO CODEC `.eac3`, `.ac3` .**
- **SUPPORT MORE VIDEO AND AUDIO CODECS AND VARIOUS EXTENSION FORMATE'S .**
- **`MediaSwift`: A VERSATILE LIBRARY WITH MANY SUPPORT AUDIO AND VIDEO CODECS, AS WELL AS MULTIPLE FILE FORMATS EXTENSION .**

- ## LIST THE AVAILABLE `.CODEC'S()`, `.FORMATE'S()` AND `.HWACCEL'S()` :

```python
from MediaSwift import *

INFO = ffpe()

print(INFO.codecs())
print(INFO.formats())
print(INFO.hwaccels())

# GET CODECS ENCODING
print(INFO.codecs(encoder='aac'))

```

- #### ENHANCE COMPATIBILITY BY LEVERAGING THE `.formats()`, `.codecs()` `.hwaccels()` AND METHODS TO VALIDATE SUPPORT FOR A VARIETY OF FORMATS, CODECS AND HARDWARE ACCELERATION .
- #### GET INFORMATION ABOUT THE CODEC'S ENCODER `.codecs(encoder="aac")` .
- ## CHECK LIBRARY VERSION USING :

```python

from MediaSwift import *

# GET AND PRINT AUTHOR INFORMATION
AUTHOR_INFO = author()
print(AUTHOR_INFO)

# GET AND PRINT VERSION INFORMATION
VERSION_INFO = version()
print(VERSION_INFO)

```

- ## EFFICIENT MEDIA PLAYBACK WITH `ffpl` .

#### THE `ffpl` CLASS PROVIDES METHODS FOR PLAY MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHOD:

```python
from MediaSwift import *

# INCREASE VOLUME BY 5 DB
PLAY = ffpl()
MEDIA_FILE = r"PATH_TO_MEDIA_FILE"                                        # PLAY SINGE MEDIA FILE
MEDIA_FILE = r"PATH_TO_MEDIA_FILE_1", r"PATH_TO_MEDIA_FILE_2"             # PLAY MULTIPLE MEDIA FILE

# USE noborder=True TO REMOVE PLAYER WINDOW BORDER.
print(PLAY.play(MEDIA_FILE, volume=5, noborder=True))
print(PLAY.play_multiple(MEDIA_FILE ,volume=5, noborder=True))
```

#### NOTE: USE THE `.play()` METHOD TO PLAY MEDIA FILES .

**`noborder=True` ARGUMENT TO ELIMINATE THE BORDER OF THE PLAYER WINDOW .**
**`volume=True` TO AMPLIFY THE AUDIO OUTPUT IN DECIBELS .**

- ## ANALYZE MEDIA FILE `ffpr`.

#### THE `ffpr` CLASS PROVIDES METHODS FOR PROBING MEDIA FILES. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS :

```python
from MediaSwift import ffpr

DETAILS = ffpr()
INFO = DETAILS.probe(r"PATH_TO_INPUT_FILE")

print(DETAILS.analyze(INFO))

# ENHANCE THE APPEALING CONTENT USING 'pretty=True'.
print(DETAILS.analyze(INFO, pretty=True))
```

**SUBSTITUTE `"PATH_TO_INPUT_FILE"` WITH THE ACTUAL FILE PATH TO YOUR MEDIA FILE. THE `.probe` METHOD RETURNS A DICTIONARY CONTAINING DETAILED INFORMATION ABOUT THE MEDIA FILE. WHEN USING `pretty=True`, THE CONTENT IS DISPLAYED IN A MORE VISUALLY APPEALING FORMAT.**

**SPECIFY `pretty=True` TO DISPLAY THE INFORMATION IN A VISUALLY ENHANCED FORMAT.**

- ## CONVERT MEDIA FILE `ffpe`.

#### `ffpe` CLASS PROVIDES METHODS FOR VIDEO CONVERSION, LISTING CODECS, AND LISTING FORMATS. HERE ARE SOME EXAMPLES OF HOW TO USE THESE METHODS :

**EXAMPLE ⇨ CONVERT SINGLE VIDEO USING THIS :**

```python
from MediaSwift import ffpe

FFMPL = ffpe()

FFMPL.convert(
    input_files = r"PATH_TO_INPUT_FILE" ,         # INPUT FILE PATH
    output_dir =  r"PATH_TO_OUTPUT_FOLDER" ,      # OUTPUT PATH
    cv='h264',        # VIDEO CODEC
    ca='aac',         # AUDIO CODEC
    s='1920x1080',    # VIDEO RESOLUTION
    hwaccel='cuda',   # HARDWARE ACCELERATION
    ar=44100,         # AUDIO SAMPLE RATE
    ac=2,             # AUDIO CHANNELS
    ba='192k',        # AUDIO BITRATE
    r=30,             # VIDEO FRAME RATE
    bv='50m',         # VIDEO BITRATE
    preset='fast',    # PRESET FOR ENCODING
    f='mp4',          # OUTPUT FORMAT

)
```

**EXAMPLE ⇨ CONVERT MULTIPLE VIDEO USING THIS :**
**⇨ NOTE : ALWAYS SET INPUT FILE PATH IN SQUARE '[ ]' BRACKETS:**

```python
from MediaSwift import ffpe

FFPE_INSTANCE = ffpe()

INPUT_FILES = [
    r"PATH_TO_INPUT_FILE",
    r"PATH_TO_INPUT_FILE",
    # ADD MORE FILE PATHS AS NEEDED
]                                                           # INPUT_FILES [MULTIPLE CONVERT]
INPUT_FILES =  r'PATH_TO_INPUT_FILE'                        # INPUT_FILES [SINGLE CONVERT]
OUTPUT_DIR =   r"PATH_TO_OUTPUT_FOLDER"

FFPE_INSTANCE.convert(
    input_files = INPUT_FILES, # INPUT FILE PATH
    output_dir = OUTPUT_DIR,   # OUTPUT PATH
    cv='h264',        # VIDEO CODEC
    ca='aac',         # AUDIO CODEC
    s='1920x1080',    # VIDEO RESOLUTION
    hwaccel='cuda',   # HARDWARE ACCELERATION
    ar=44100,         # AUDIO SAMPLE RATE
    ac=2,             # AUDIO CHANNELS
    ba='192k',        # AUDIO BITRATE
    bv='50m',         # VIDEO BITRATE
    preset='fast',    # PRESET FOR ENCODING
    r=30,             # VIDEO FRAME RATE
    f='mp4',          # OUTPUT FORMAT
)
```

#### EXAMPLE ⇨ CONVERT MULTIPLE VIDEO INTO AUDIO FILE USING THIS :

```python

from MediaSwift import ffpe
FFPE_INSTANCE = ffpe()

# DEFINE INPUT FILES AND OUTPUT DIRECTORY.
INPUT_FILES = [ r'PATH_TO_INPUT_FILE', r'PATH_TO_INPUT_FILE' ]     # INPUT_FILES [MULTIPLE CONVERT]
INPUT_FILES =   r'PATH_TO_INPUT_FILE'                              # INPUT_FILES [SINGLE CONVERT]

OUTPUT_DIR =  r"PATH_TO_OUTPUT_FOLDER"

# PERFORM MULTIMEDIA FILE CONVERSION USING FFPE.
FFPE_INSTANCE.convert(
    input_files=INPUT_FILES,
    output_dir=OUTPUT_DIR ,
    hwaccel="cuda",   # HARDWARE ACCELERATION
    ar=44100,         # AUDIO SAMPLE RATE
    ac=2,             # AUDIO CHANNELS
    ba="192k",        # AUDIO BITRATE
    f="mp3",          # OUTPUT FORMAT (MP3 for audio)
)

```

#### ⇨ NOTE : USE THE `.convert()` METHOD TO CONVERT MEDIA FILES .

**NOTE ⇨ ALWAYS SET MULTIPLE INPUT_FILES PATH IN SQUARE '[ ]' BRACKETS:**

```python

from MediaSwift import *

CONVERTER = ffpe()
INPUT_FILE = r"PATH_TO_INPUT_FILE"  # INPUT FILE
OUTPUT_FILE = r"PATH_TO_INPUT_FILE"  # OUTPUT FILE
TIME_RANGE = "01:30,02:30"  # CLIP FROM 1 MINUTE 30 SECONDS TO 2 MINUTES 30 SECONDS

CONVERTER.MediaClip(INPUT_FILE, OUTPUT_FILE, TIME_RANGE)

```

**NOTE : USE THE `.MediaClip()` METHOD TO EXTRACTS SPECIFIC PART OF VIDEO AND CONVERTS IT INTO GIF.**

- ## 🔎 IMPORT CLASSES AND MODULE :

```python
from MediaSwift import ffpe, ffpl, ffpr
from MediaSwift import *
```

- ## ⚙️ INSTALLATION :

```bash
pip install MediaSwift
```

- ## 😃 AUTHOR INFORMATION :

**THIS PYTHON LIBRARY PROJECT IS DONE BY `ROHIT SINGH` . FOR ANY QUERIES TO CHECK MY GITHUB, THANK YOU FOR USING `MediaSwift` PYTHON LIBRARY,LIBRARY RELEASE IN 2024 .**

[![GitHub Profile](https://img.shields.io/badge/GitHub-ROHIT%20SINGH-blue?style=flat-square&logo=github)](https://github.com/ROHIT-SINGH-1)
