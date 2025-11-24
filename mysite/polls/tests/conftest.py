import pytest
import datetime as dt
from django.utils import timezone

from polls.models import Question


@pytest.fixture()
def create_question(db):
    def _create(pub_date=None, text: str = "recent question"):
        if pub_date is None:
            pub_date = timezone.now()

        return Question.objects.create(
            question_text=text,
            pub_date=pub_date,
        )

    return _create

@pytest.fixture()
def fixed_now(mocker):
    value = dt.datetime(2025, 1, 1, 12, 0, tzinfo=timezone.get_current_timezone())
    mocker.patch("django.utils.timezone.now", return_value=value)
    return value
