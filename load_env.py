from os import environ
from dotenv import load_dotenv

_LOAD = False


def load_env():
    global _LOAD
    if not _LOAD and environ.get("PRODUCTION") is None or environ.get("PRODUCTION") == "false":
        load_dotenv()
        _LOAD = True
