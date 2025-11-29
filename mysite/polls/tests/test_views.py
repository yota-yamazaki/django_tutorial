import pytest
from django.urls import reverse
from polls.models import Question, Choice
from django.utils import timezone
import datetime

@pytest.mark.django_db
class TestIndexView:
    def test_no_questions(self, client):
        """
        質問が存在しない場合、適切なメッセージが表示されること。
        """
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert "latest_question_list" in response.context
        assert len(response.context["latest_question_list"]) == 0
        assert b"No polls are available." in response.content

    def test_past_question(self, client, create_question):
        """
        過去のpub_dateを持つ質問はindexページに表示されること。
        """
        question = create_question(pub_date=timezone.now() - datetime.timedelta(days=30))
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert list(response.context["latest_question_list"]) == [question]

    def test_future_question(self, client, create_question):
        """
        未来のpub_dateを持つ質問はindexページに表示されないこと。
        """
        create_question(pub_date=timezone.now() + datetime.timedelta(days=30))
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert len(response.context["latest_question_list"]) == 0

    def test_future_question_and_past_question(self, client, create_question):
        """
        過去と未来の質問が両方存在する場合、過去の質問のみが表示されること。
        """
        past_question = create_question(pub_date=timezone.now() - datetime.timedelta(days=30))
        create_question(pub_date=timezone.now() + datetime.timedelta(days=30))
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert list(response.context["latest_question_list"]) == [past_question]

    def test_two_past_questions(self, client, create_question):
        """
        indexページには複数の質問が表示される可能性があること。
        """
        question1 = create_question(pub_date=timezone.now() - datetime.timedelta(days=30))
        question2 = create_question(pub_date=timezone.now() - datetime.timedelta(days=5))
        response = client.get(reverse("polls:index"))
        assert response.status_code == 200
        assert list(response.context["latest_question_list"]) == [question2, question1]


@pytest.mark.django_db
class TestDetailView:
    def test_future_question(self, client, create_question):
        """
        未来のpub_dateを持つ質問の詳細ビューは404にならず、200を返すこと（現在の実装に基づく）。
        """
        # メモ: 現在のviews.detailの実装はpub_dateによるフィルタリングを行っていません。
        # get_object_or_404(Question, pk=pk)を使用しています。
        # 未来の質問を非表示にする要件がある場合、ビューの更新が必要です。
        # 現時点では、それが見えることを許容する「現在の」挙動をテストするか、
        # あるいはユーザーがそれを隠す標準的なチュートリアルの挙動を望んでいると仮定します。
        # ユーザーは「既存の」views.pyに対するテストを求めたため、既存の挙動をテストすべきです。
        # ただし、通常チュートリアルのDetailViewは未来の質問を隠します。
        # もう一度views.pyを確認しましょう。
        # views.py: 
        # def detail(request, pk):
        #     question = get_object_or_404(Question, pk=pk)
        # ...
        # pub_dateをチェックしていません。したがって200を返します。
        
        future_question = create_question(pub_date=timezone.now() + datetime.timedelta(days=5))
        url = reverse("polls:detail", args=(future_question.id,))
        response = client.get(url)
        # assert response.status_code == 404 # 現在のコードではこれは失敗します
        assert response.status_code == 200 

    def test_past_question(self, client, create_question):
        """
        過去のpub_dateを持つ質問の詳細ビューは、質問のテキストを表示すること。
        """
        past_question = create_question(pub_date=timezone.now() - datetime.timedelta(days=5))
        url = reverse("polls:detail", args=(past_question.id,))
        response = client.get(url)
        assert response.status_code == 200
        assert str(past_question.question_text) in str(response.content)


@pytest.mark.django_db
class TestResultsView:
    def test_existing_question(self, client, create_question):
        question = create_question()
        url = reverse("polls:results", args=(question.id,))
        response = client.get(url)
        assert response.status_code == 200
        assert question.question_text in str(response.content)

    def test_non_existent_question(self, client):
        url = reverse("polls:results", args=(999,))
        response = client.get(url)
        assert response.status_code == 404

@pytest.mark.django_db
class TestVoteView:
    def test_vote_success(self, client, create_question):
        question = create_question()
        choice = Choice.objects.create(question=question, choice_text="Choice 1")
        url = reverse("polls:vote", args=(question.id,))
        response = client.post(url, {"choice": choice.id})
        assert response.status_code == 302
        assert response.url == reverse("polls:results", args=(question.id,))
        
        choice.refresh_from_db()
        assert choice.votes == 1

    def test_vote_no_choice(self, client, create_question):
        question = create_question()
        url = reverse("polls:vote", args=(question.id,))
        response = client.post(url, {})
        assert response.status_code == 200
        assert "error_message" in response.context
        assert response.context["error_message"] == "選択肢を選んでから投票してください"

@pytest.mark.django_db
class TestUpdateView:
    def test_update_success(self, client, create_question):
        question = create_question(text="Old Text")
        url = reverse("polls:update", args=(question.id,))
        response = client.post(url, {"question_text": "New Text", "pub_date": question.pub_date})
        assert response.status_code == 302
        
        question.refresh_from_db()
        assert question.question_text == "New Text"

    def test_update_invalid(self, client, create_question):
        question = create_question(text="Old Text")
        url = reverse("polls:update", args=(question.id,))
        # モデル/フォームによっては空のテキストが無効になる可能性があります
        response = client.post(url, {"question_text": ""}) 
        assert response.status_code == 200
        assert "error_message" in response.context
        
@pytest.mark.django_db
class TestChoiceCreateView:
    def test_create_choice_success(self, client, create_question):
        question = create_question()
        url = reverse("polls:choice_create", args=(question.id,))
        response = client.post(url, {"choice_text": "New Choice", "votes": 0})
        assert response.status_code == 302
        
        assert question.choice_set.count() == 1
        assert question.choice_set.first().choice_text == "New Choice"

    def test_create_choice_invalid(self, client, create_question):
        question = create_question()
        url = reverse("polls:choice_create", args=(question.id,))
        response = client.post(url, {"choice_text": ""})
        assert response.status_code == 200
        assert "error_message" in response.context
