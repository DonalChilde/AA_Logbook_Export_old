from pathlib import Path
from typing import Any
import json
import logging

#### setting up logger ####
logger = logging.getLogger(__name__)

#### Log Level ####
# NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
# log_level = logging.DEBUG
# log_level = logging.INFO
log_level = logging.NOTSET
logger.setLevel(log_level)

#### Log Handler ####
log_formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
# logger.addHandler(log_handler)


def loadJson(path: Path) -> Any:
    try:
        with open(path, "r") as jsonFile:
            data = json.load(jsonFile)
        return data
    except Exception as e:
        logger.exception(f"Error trying to load json file from {path}")
        raise e


def saveJson(data: Any, path: Path, indent=2, sort_keys=False) -> bool:

    try:
        with open(path, "w") as jsonFile:
            json.dump(data, jsonFile, indent=indent, sort_keys=sort_keys)
        return True
    except Exception as e:
        logger.exception(f"Error trying to save json data to {path}")
        raise e
