import ast
import datetime
import logging
import typing

from aind_data_schema.core import rig

from np_aind_metadata import common
from np_aind_metadata.init import neuropixels_rig

logger = logging.getLogger(__name__)

try:
    import np_config
except Exception:
    logger.error("Failed to import neuropixels-related dependencies.", exc_info=True)


# cannot type hint due to np import failing in github actions
def _get_rig_config(rig_name: common.RigName):
    return np_config.Rig(ast.literal_eval(rig_name[-1]))


def get_manipulator_infos(
    rig_name: common.RigName,
) -> list[common.ManipulatorInfo]:
    return [
        common.ManipulatorInfo(
            assembly_name=f"Ephys Assembly {key}",
            serial_number=value,
        )
        for key, value in _get_rig_config(rig_name)
        .config["services"]["NewScaleCoordinateRecorder"]["probe_to_serial_number"]
        .items()
    ]


def init_neuropixels_rig_from_np_config(
    rig_name: common.RigName,
    modification_date: typing.Optional[datetime.date] = None,
) -> rig.Rig:
    """Initializes a rig model using settings from np_config.

    Notes
    -----
    - Might require you to be onprem to connect to np_config's zookeeper
     server.
    """
    rig_config = _get_rig_config(rig_name)
    return neuropixels_rig.init(
        rig_name,
        mon_computer_name=rig_config.Mon,
        stim_computer_name=rig_config.Stim,
        sync_computer_name=rig_config.Sync,
        modification_date=modification_date,
    )
