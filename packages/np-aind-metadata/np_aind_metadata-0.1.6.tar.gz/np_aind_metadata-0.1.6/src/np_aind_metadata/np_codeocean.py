import logging
import pathlib
import shutil
import tempfile

from aind_data_schema.core import rig, session

from np_aind_metadata import storage
from np_aind_metadata.update import dynamic_routing_task as dynamic_routing_task_update

logger = logging.getLogger(__name__)


def scrape_session_model_path(session_directory: pathlib.Path) -> pathlib.Path:
    """Scrapes aind-metadata session json from dynamic routing session
    directory.
    """
    matches = list(session_directory.glob("*session.json"))
    logger.debug("Scraped session model paths: %s" % matches)
    return matches[0]


def _update_session_rig_id(
    session: session.Session,
    rig_id: str,
    output_path: pathlib.Path,
) -> pathlib.Path:
    """Updates session rig id and copies it to `output_path`."""
    session.rig_id = rig_id
    with tempfile.TemporaryDirectory() as temp_dir:
        session.write_standard_file(temp_dir)
        temp_session_path = pathlib.Path(temp_dir) / session.default_filename()
        assert temp_session_path.exists()
        return pathlib.Path(shutil.copy2(temp_session_path, output_path))


def add_rig_to_dynamic_routing_session_dir(
    session_dir: pathlib.Path,
    rig_model_dir: pathlib.Path,
) -> pathlib.Path:
    """Direct support for np_codeocean. Adds an aind-metadata rig model
    rig.json to a dynamic routing session directory. If rig_id is updated,
     will update the associated session json.

    Notes
    -----
    - An aind metadata session json must exist and be ending with filename
    session.json (pattern: `*session.json`) in the root directory.
    """
    scraped_session_model_path = scrape_session_model_path(session_dir)
    scraped_session = session.Session.model_validate_json(
        scraped_session_model_path.read_text()
    )
    scraped_rig_id = scraped_session.rig_id
    logger.info("Scraped rig id: %s" % scraped_rig_id)
    _, rig_name, _ = scraped_rig_id.split("_")
    logger.info("Parsed rig name: %s" % rig_name)
    current_model_path = storage.get_item(
        rig_model_dir,
        rig_name,
        "dynamic-routing",
    )
    logger.info("Current model path: %s" % current_model_path)
    settings_sources = list(session_dir.glob("**/settings.xml"))
    logger.info("Scraped open ephys settings: %s" % settings_sources)

    if settings_sources:
        logger.debug("Updating model.")
        current_model = rig.Rig.model_validate_json(current_model_path.read_text())
        current_model.write_standard_file(session_dir)
        session_rig_path = session_dir / "rig.json"
        assert (
            session_rig_path.exists()
        ), "Session rig path should exist where we expect."
        updated_model_path = dynamic_routing_task_update.update_rig(
            session_rig_path,
            open_ephys_settings_sources=settings_sources,
            output_path=session_rig_path,
        )
        updated_model = rig.Rig.model_validate_json(updated_model_path.read_text())
        if updated_model.rig_id != scraped_rig_id:
            logger.debug("Rig model rig_id has changed. Updating session rig_id.")
            _update_session_rig_id(
                scraped_session,
                updated_model.rig_id,
                scraped_session_model_path,
            )
        if current_model != updated_model:
            logger.debug("Current rig model has changed. Updating storage.")
            storage.update_item(
                rig_model_dir,
                updated_model_path,
                rig_name,
                "dynamic-routing",
            )

    return updated_model_path
