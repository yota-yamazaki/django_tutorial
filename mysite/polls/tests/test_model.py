import pytest

@pytest.mark.django_db
@pytest.mark.parametrize(
    ["time", "expect"],
    [
        pytest.param(1, True, id="1h old"),
        pytest.param(24, True, id="24h old"),
        pytest.param(25, False, id="25h old"),
        pytest.param(0, True, id="now"),
        pytest.param(-1, False, id="1h future"),
    ],
)
def test_was_published_recently(create_question, expect):
    assert create_question.was_published_recently() is expect
