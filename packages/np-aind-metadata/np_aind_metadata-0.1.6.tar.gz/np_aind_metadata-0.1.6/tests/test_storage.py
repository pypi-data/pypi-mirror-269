import json
import pathlib

import pytest

from np_aind_metadata import storage


@pytest.mark.storage
def test_update_get_update_get(
    tmp_path: pathlib.Path
) -> None:
    item_0 = {
        "rig_id": "327_NP1_240401",
    }
    item_0_path = tmp_path / "item-0.json"
    item_0_path.write_text(json.dumps(item_0))
    tags = ("NP1", "dynamic-routing")
    storage.update_item(
        tmp_path,
        item_0_path,
        *tags,
    )
    stored_item = json.loads(storage.get_item(
        tmp_path,
        *tags,
    ).read_text())
    assert stored_item == item_0, \
        "Stored item is what we expect."
    item_1 = {
        "rig_id": "327_NP1_240402",
    }
    item_1_path = tmp_path / "item-1.json"
    item_1_path.write_text(json.dumps(item_1))
    storage.update_item(
        tmp_path,
        item_1_path,
        *tags,
    )
    updated_item = json.loads(storage.get_item(
        tmp_path,
        *tags,
    ).read_text())
    assert updated_item != item_0, \
        "Stored item is not previous."
    assert updated_item == item_1, "Stored item is updated item."
