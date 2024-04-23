"""Stores a history of object changes in local storage.
Simple updater and getter for iterations of a file.
"""

import ast
import json
import logging
import pathlib
import shutil
import time

logger = logging.getLogger(__name__)


def _generate_item_filename(
    *tags: str,
) -> str:
    return "_".join(str(tag) for tag in tags)


def _item_path_sorter(path: pathlib.Path) -> int:
    mtime_str = path.stem.split("_")[-1]
    return ast.literal_eval(mtime_str)


def get_item(
    storage_directory: pathlib.Path,
    *_tags: str,
) -> pathlib.Path:
    """"""
    search_pattern = _generate_item_filename(*_tags, "*")
    logger.info("Search pattern: %s" % search_pattern)
    items = list(storage_directory.glob(search_pattern))
    if not items:
        raise Exception("No item found for tags: %s" % json.dumps(_tags))

    sorted_items = sorted(items, key=_item_path_sorter)
    logger.debug("Fetched items: %s" % sorted_items)
    return sorted_items[-1]


def update_item(
    storage_directory: pathlib.Path,
    filepath: pathlib.Path,
    *_tags: str,
):
    """
    Notes
    -----
    - Also used to initialize a new base rig in local storage.
    - If a rig with the same name doest not exist, a new rig will be created.
    """
    filename = _generate_item_filename(*_tags, str(int(time.time())))

    return shutil.copy2(
        filepath,
        storage_directory / filename,
    )
