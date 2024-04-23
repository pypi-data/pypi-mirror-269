import datetime
import logging
import os
import pathlib
import tempfile
import typing

import click

from np_aind_metadata import common, np, storage, utils
from np_aind_metadata.update import dynamic_routing_task as dynamic_routing_task_update

logger = logging.getLogger(__name__)


NPEXP_PATH_ROOT = os.getenv("NPEXP_PATH_ROOT")
now = datetime.datetime.now()


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.option("--log-file", default=False, is_flag=True)
def cli(debug: bool, log_file: bool) -> None:
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    if debug:
        np.logger.setLevel(logging.DEBUG)
        storage.logger.setLevel(logging.DEBUG)
        dynamic_routing_task_update.logger.setLevel(logging.DEBUG)
        utils.logger.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)

    if log_file:
        handler = logging.FileHandler(
            now.strftime("np-aind-metadata_%Y-%m-%d-%H-%M-%S") + ".log"
        )
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)
        np.logger.addHandler(handler)
        storage.logger.addHandler(handler)
        dynamic_routing_task_update.logger.addHandler(handler)
        utils.logger.addHandler(handler)


modification_date_format_0 = "%Y-%m-%d"
modification_date_format_1 = "%Y/%m/%d"


@cli.command()
@click.argument("storage-directory", type=pathlib.Path)
@click.argument(
    "rig-name",
    type=click.Choice(["NP1", "NP2", "NP3"]),
)
@click.option(
    "--date",
    help=(
        "Rig modification date. Supported formats:"
        f" {modification_date_format_0}, {modification_date_format_1}"
    ),
    type=click.DateTime(
        formats=[
            modification_date_format_0,
            modification_date_format_1,
        ]
    ),
)
def init_rig_storage(
    storage_directory: pathlib.Path,
    rig_name: common.RigName,
    date: typing.Optional[datetime.datetime] = None,
) -> None:
    if date is None:
        modification_date = None
    else:
        modification_date = date.date()

    with tempfile.TemporaryDirectory() as temp_dir:
        rig_model = np.init_neuropixels_rig_from_np_config(
            rig_name=rig_name,
            modification_date=modification_date,
        )
        rig_model.write_standard_file(temp_dir)
        rig_model_path = pathlib.Path(temp_dir) / "rig.json"
        added_path = storage.update_item(
            storage_directory,
            rig_model_path,
            rig_name,
            "dynamic-routing",
        )
        logger.debug("Stored rig model at: %s" % added_path)

    click.echo("Initialized rig storage for: %s" % rig_name)


if __name__ == "__main__":
    cli()
