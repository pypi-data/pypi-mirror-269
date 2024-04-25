import pytest

from np_upload_validation import npc


@pytest.mark.onprem
@pytest.mark.parametrize("args, expected", [
    (("DRpilot_686176_20231207", ), True),
    (("686176_2023-12-07", ), True),
    (("hopefully-not-an-id", ), False),
])
def test_is_session_id(args, expected) -> None:  # noqa: ANN001
    assert npc.is_session_id(*args) == expected
