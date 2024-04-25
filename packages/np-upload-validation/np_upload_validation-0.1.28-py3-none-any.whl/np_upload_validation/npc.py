import logging
import typing

import npc_lims
import npc_sessions

from . import models

logger = logging.getLogger(__name__)

# try:
#     import np_session
# except Exception:
#     logger.error("Failed to import np-session.", exc_info=True)


def get_uploaded_timing_data_paths(
    session_id: str,
) -> typing.Union[list[models.UploadedTimingData], None]:
    info = npc_lims.get_session_info(
        session=session_id,
    )
    if not info.is_uploaded:
        logger.debug("Data not yet uploaded.")
        return None

    _id = info.id
    if session_id.endswith("_surface_channels"):
        _id = _id.with_idx(1)
    session = npc_sessions.Session(_id)

    timing_data = []
    for timing_info in session.ephys_timing_data:
        device_name = timing_info.device.name
        path = timing_info.device.compressed
        if not path:
            logger.debug("No compressed timing data path for %s." % device_name)
            continue
        timing_data.append(
            models.UploadedTimingData(
                device_name=device_name,
                path=path,
            )
        )

    return timing_data


# def is_session_id(_id: str) -> bool:
#     try:
#         np_session.Session(_id)
#         return True
#     except np_session.SessionError:
#         logger.debug("Invalid session ID: %s" % _id, exc_info=True)
#         return False


def is_session_id(_id: str) -> bool:
    try:
        npc_lims.get_session_info(session=_id)
        return True
    except Exception:
        logger.debug("Invalid session ID: %s" % _id, exc_info=True)
        return False
