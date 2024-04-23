# config/settings.py

import os
from pathlib import Path

# Plugin metadata
PLUGIN_NAME = "YaraForge"
PLUGIN_DIR_NAME = "yaraforge"
AUTHORS = [
    {"name": "Zhao Xinn", "email": "zhaoxinzhang0429@gmail.com"},
    {"name": "Tsai YA-HSUAN", "email": "aooood456@gmail.com"},
    {"name": "Ting0525", "email": "zg45154551@gmail.com"},
]
GITHUB_URL = "https://github.com/zhaoxinnZ/YaraForge"
DESCRIPTION = "A plugin for IDA Pro to generate Yara rules from binary files."

# Version requirements
PYTHON_REQUIRES = ">=3.8, <3.12"
IDAPYTHON_REQUIRES = ">=7.0"
CAPA_VERSION = "7.0.1"

# Paths
APPDATA_ROAMING = Path(os.getenv('APPDATA'))
PLUGIN_PATH = APPDATA_ROAMING / "Hex-Rays" / "IDA Pro" / "plugins"
YARAFORGE_BASE_DIR = PLUGIN_PATH / PLUGIN_DIR_NAME

PATHNAMES = {
    "yaraforge_dir": YARAFORGE_BASE_DIR,
    "cache_dir": YARAFORGE_BASE_DIR / "cache",
    "results_dir": YARAFORGE_BASE_DIR / "cache/results",
    "pretty_dump_dir": YARAFORGE_BASE_DIR / "cache/results/pretty_dump",
    "instructions_dir": YARAFORGE_BASE_DIR / "cache/results/instructions",
    "yara_rules_dir": YARAFORGE_BASE_DIR / "cache/results/yara_rules",
    "logger_dir": YARAFORGE_BASE_DIR / "logs",
}

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - [%(filename)s] - %(levelname)s - %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"