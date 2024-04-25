import logging
import pathlib

import numpy as np
import upath
import zarr

from . import models

logger = logging.getLogger(__name__)


def get_dat_info(path: pathlib.Path) -> models.ArrayInfo:
    arr = np.memmap(
        path,
        dtype=np.int16,
        mode="r",
    )
    return models.ArrayInfo(
        path=path.as_posix(),
        size=arr.size,
        dtype=str(arr.dtype),
    )


def get_zarr_info(path: upath.UPath) -> models.ArrayInfo:
    arr = zarr.open(path, mode="r")["traces_seg0"]
    return models.ArrayInfo(
        path=path.as_posix(),
        size=arr.size,
        dtype=str(arr.dtype),
    )


def pair_timing_data(
    uploaded: list[models.UploadedTimingData], local: list[pathlib.Path]
) -> list[tuple[models.UploadedTimingData, list[pathlib.Path]]]:
    """Pairs uploaded and local timing data."""
    paired = []
    for uploaded_timing_data in uploaded:
        associated_local = list(
            filter(
                lambda x: uploaded_timing_data.device_name in str(x),
                local,
            )
        )
        if associated_local:
            paired.append((uploaded_timing_data, associated_local))
        else:
            logger.debug(
                "No local timing data found for %s." % uploaded_timing_data.device_name
            )

    return paired
