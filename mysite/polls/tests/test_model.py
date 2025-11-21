import datetime

import pytest
from django.utils import timezone

from polls.models import Question

@pytest.mark.parametrize(
    ["time", "is_recently"],
    [
        pytest.param(0, True, id="now"),
        pytest.param(24, True, id="24h later"),
        pytest.param(25, False, id="25h later"),
        pytest.param(-1, False, id="1h future"),
    ],
)
@pytest.mark.django_db
def test_was_published_recently(freezer, time, is_recently):
    pub_date = timezone.now() - datetime.timedelta(hours=time)

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is is_recently
