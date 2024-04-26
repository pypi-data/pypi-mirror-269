import sys
from pathlib import Path


def to_absolute_path(relative_path: str) -> Path:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        script_dir = Path(sys._MEIPASS)
    else:
        script_dir = Path(__file__).parent

    return script_dir / relative_path
