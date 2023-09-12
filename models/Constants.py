import os
DEFAULT_CONFIG: dict={"dir": "", "spotify_enabled": False, "prefs": {"font": ["Arial", 14, "normal", "roman", 0, 0], "parallel": False, "print_log": True, "theme": "vista", "verbosity": False, "remove_success": False, "rerun": False, "outwin_mode": 1, "update_launch": True, "disable_stats": False, "disable_percentage": False}, "opts": {"resolution": 1080, "subtitles": True, "metadata": True, "thumbnail": True, "description": False, "audio": False, "video_format": "best", "audio_format": "best", "strict_format": False, "format_string": "", "output_template": ""}}

DATA_PATH = os.path.abspath(os.path.expandvars("%appdata%\\Youtube-dl_GUI"))

THUMBNAIL_VIDEO_FORMATS = ["best",
"avi",                       
"mkv",
"mov",
"mp4"
]

THUMBNAIL_AUDIO_FORMATS = ["best",
"flac",
"ogg",
"opus",
"m4a",
"mka",
"mp3"
]

RESOLUTION_VALUES=[144, 240, 480, 720, 1080, 1440, 2160, 4320]

VIDEO_FORMATS = ["best", "mp4", "mkv", "webm"]

AUDIO_FORMATS=["best", "mp3", "wav", "m4a", "ogg"]

COMPATIBLE_FORMATS = {"mp4": ['m4a', 'mp3'], "webm": ['ogg', 'opus', 'webm'], "mkv": ['mka', 'opus', 'flac', 'mp3', 'wav', 'webm']}