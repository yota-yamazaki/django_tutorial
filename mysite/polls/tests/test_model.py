import pytest
import datetime as dt
from django.utils import timezone

# fixtureのfixed_nowはtimezone.nowの時間を固定する
@pytest.mark.django_db
@pytest.mark.parametrize(
    ["hours", "expect"],
    [
        pytest.param(1, True, id="1h old"),
        pytest.param(24, True, id="24h old"),
        pytest.param(25, False, id="25h old"),
        pytest.param(0, True, id="now"),
        pytest.param(-1, False, id="1h future"),
    ],
)
def test_was_published_recently(hours, expect, create_question, fixed_now):
    pub_date = timezone.now() - dt.timedelta(hours=hours)

    assert create_question(pub_date).was_published_recently() is expect
