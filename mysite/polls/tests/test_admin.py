import datetime as dt
import pytest
from django.utils import timezone
from polls.models import Question, Choice, Reservation
from polls.admin import QuestionAdmin, polls_admin_site
from django.urls import reverse

# fixtureのfixed_nowはtimezone.nowの時間を固定する
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
def test_was_published_recently(admin_client, hours, expect, create_question, fixed_now):
    pub_date = timezone.now() - dt.timedelta(hours=hours)

    create_question(pub_date)

    url = reverse("polls_admin:polls_question_changelist")
    response = admin_client.get(url)

    assert response.status_code == 200

    if expect:
        assert b"icon-yes.svg" in response.content
    else:
        assert b"icon-no.svg" in response.content

@pytest.mark.django_db
def test_choice_list_at_question_change(admin_client, create_question):
    q = create_question()

    ary = ["A", "B", "C"]
    for a in ary:
        Choice.objects.create(
            question=q,
            choice_text=a,
            votes=0,
        )

    url = reverse("polls_admin:polls_question_change", args=[q.pk])
    response = admin_client.get(url)

    assert response.status_code == 200

    assert b'value="A"' in response.content
    assert b'value="B"' in response.content
    assert b'value="C"' in response.content

def test_choice_list(create_question):
    q = create_question()

    ary = ["A", "B", "C"]
    for a in ary:
        Choice.objects.create(
            question=q,
            choice_text=a,
            votes=0,
        )

    admin = QuestionAdmin(Question, polls_admin_site)
    cl = admin.choice_list(q)

    assert cl == ["A", "B", "C"]

@pytest.mark.parametrize(
    ["status",],
    [
        pytest.param("予約"),
        pytest.param("チェックイン"),
        pytest.param("完了"),
    ],
)
def test_get_readonly_fields(admin_client, status, create_question):
    q = create_question()

    Reservation.objects.create(
        question=q,
        reservation_number="12345",
        status=status,
    )

    url = reverse("polls_admin:polls_question_change", args=[q.pk])
    response = admin_client.get(url)


