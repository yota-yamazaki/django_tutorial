import datetime

import pytest
from django.utils import timezone

from polls.models import Question

@pytest.mark.django_db
def test_was_published_recently_with_recent_question():
    pub_date = timezone.now() - datetime.timedelta(hours=23)
    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is True

@pytest.mark.django_db
def test_was_published_recently_with_not_recent_question():
    pub_date = timezone.now() - datetime.timedelta(hours=25)

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is False

@pytest.mark.django_db
def test_was_published_recently_with_future_question():
    pub_date = timezone.now() + datetime.timedelta(hours=1)

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is False

# freezerテクスチャによってnowが固定されるので、ジャスト24h前ならTrue
@pytest.mark.django_db
def test_was_published_recently_with_24h_question(freezer):
    pub_date = timezone.now() - datetime.timedelta(hours=24)

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is True

# ちょうど今
@pytest.mark.django_db
def test_was_published_recently_with_now_question(freezer):
    pub_date = timezone.now()

    q = Question.objects.create(
        question_text="recent question",
        pub_date=pub_date,
    )

    assert q.was_published_recently() is True
