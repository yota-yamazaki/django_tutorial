import pytest
from django.utils import timezone
import datetime

from polls.models import Question

@pytest.fixture()
def create_question(freezer, time, db):
    pub_date = timezone.now() - datetime.timedelta(hours=time)

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    return q

