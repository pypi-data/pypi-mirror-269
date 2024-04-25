import datetime
import logging
import pathlib
import typing

from . import local as local_utils
from . import models, npc, utils

logger = logging.getLogger(__name__)


def _arrays_match(local: models.ArrayInfo, uploaded: models.ArrayInfo) -> bool:
    return local.size == uploaded.size and local.dtype == uploaded.dtype


def infer_associated(
    local: list[models.ArrayInfo], uploaded: models.ArrayInfo
) -> models.AssociatedArrays:

    if len(local) > 1:
        for local_info in local:
            if _arrays_match(local_info, uploaded):
                associated_local = local_info
                break
        else:
            associated_local = local[0]
    else:
        associated_local = local[0]

    return models.AssociatedArrays(
        local=associated_local,
        uploaded=uploaded,
        match=_arrays_match(associated_local, uploaded),
    )


def validate(
    session_id: str, exp_dir_root: pathlib.Path
) -> typing.Union[list[models.UploadIntegrity], None]:
    """Validate the size and dtype of uploaded timing data arrays."""
    uploaded = npc.get_uploaded_timing_data_paths(session_id)
    if uploaded is None:
        logger.debug("No uploaded timing data found.")
        return None

    local = local_utils.get_local_timing_data_paths(exp_dir_root, session_id)
    paired = utils.pair_timing_data(uploaded, local)

    validated = []
    for paired_uploaded, paired_local in paired:
        local_info = [utils.get_dat_info(path) for path in paired_local]
        uploaded_info = utils.get_zarr_info(paired_uploaded.path)
        validated.append(
            models.UploadIntegrity(
                session_id=session_id,
                timestamp=datetime.datetime.now().isoformat(),
                local=local_info,
                uploaded=uploaded_info,
                associated=infer_associated(local_info, uploaded_info),
            )
        )

    return validated


def batch_validate_sessions(
    exp_dir_root: pathlib.Path,
) -> typing.Generator[list[models.UploadIntegrity], None, None]:
    for exp_dir in exp_dir_root.iterdir():
        inferred_session_id = exp_dir.stem
        if npc.is_session_id(inferred_session_id):
            try:
                validated = validate(inferred_session_id, exp_dir_root)
                if validated is not None:
                    yield validated
            except Exception:
                logger.error(
                    "Failed to validate inferred session id: %s" % inferred_session_id,
                    exc_info=True,
                )
                continue
