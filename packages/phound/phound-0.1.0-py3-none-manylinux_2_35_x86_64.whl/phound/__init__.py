from dotenv import load_dotenv as _load_dotenv

from phound.main import Phound
from phound.logging import setup_logging as _setup_logging

_load_dotenv()
_setup_logging()

__all__ = ["Phound"]
