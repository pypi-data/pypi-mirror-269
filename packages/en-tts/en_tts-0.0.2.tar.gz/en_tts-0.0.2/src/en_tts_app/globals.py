from importlib.metadata import version
from pathlib import Path
from tempfile import gettempdir

APP_NAME = "en-tts"

APP_VERSION = version(APP_NAME)


def get_conf_dir() -> Path:
  conf_dir = Path.home() / ".en-tts"
  return conf_dir


def get_work_dir() -> Path:
  work_dir = Path(gettempdir()) / "en-tts"
  return work_dir


def get_log_path() -> Path:
  return Path(gettempdir()) / "en-tts.log"
