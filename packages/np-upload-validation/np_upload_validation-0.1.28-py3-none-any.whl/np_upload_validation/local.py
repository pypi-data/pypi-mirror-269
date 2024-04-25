import pathlib


def get_local_timing_data_paths(
    exp_dir_root: pathlib.Path, session_id: str
) -> list[pathlib.Path]:
    """Scrapes a local directory for timing data files."""
    exp_dir = exp_dir_root / session_id
    return list(exp_dir.glob("**/continuous.dat"))
