from dataclasses import fields
from django import forms
from . import models
from django.core.exceptions import ValidationError
from .models import Question, Reservation



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ["choice_text"]

    def clean_choice_text(self):
        choice_text = self.cleaned_data['choice_text']
        if "piyo" in choice_text:
            raise forms.ValidationError("テキストにはpiyoを入れないでください")
        return choice_text

class ChoiceAdminForm(ChoiceForm):
    pass

    class Meta(ChoiceForm.Meta):
        fields = ["choice_text", "question"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ["question_text",]

    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        if "piyo" in question_text:
            raise forms.ValidationError("テキストにはpiyoを入れないでください")
        return question_text

class QuestionEditForm(QuestionForm):
    pass

class QuestionAdminForm(QuestionForm):
    pass

    class Meta(QuestionForm.Meta):
        labels = {
                "pub_date": "発行日",
        }
        help_texts = {
                "pub_date": "注意: <strong>pub_date</strong> は必須項目です",
        }
    # adminモデルのfieldsetsのフォームが優先されるので、編集可能なフィールドはadminモデル側で

class ReservationInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        # 親がまだ存在しない場合（新規作成中など）はスキップ
        if not self.instance.pk:
            return

        # 「元の question_text」と「変更後」を比較
        old_obj = Question.objects.get(pk=self.instance.pk)
        question_text_changed = old_obj.question_text != self.instance.question_text

        if not question_text_changed:
            return

        # 画面上のインライン入力 + 既存の予約を考慮して判定したいなら、
        # ここで self.forms / self.instance.reservation_set の両方を見る
        if self.instance.reservation_set.filter(status__in=["予約", "チェックイン"]).exists():
            raise ValidationError(
                "この設問に対して「予約」または「チェックイン」の予約を追加する場合、タイトルは変更できません。"
            )

        # この POST で扱っている全ての中間レコードをチェック
        for form in self.forms:
            if not hasattr(form, "cleaned_data"):
                continue
            if form.cleaned_data.get("DELETE", False):
                continue

            # 中間テーブルの reservation FK を取得
            reservation = (
                form.cleaned_data.get("reservation")
                or getattr(form.instance, "reservation", None)
            )

            if not reservation:
                continue

            if reservation.status in [Reservation.Status.RESERVED, Reservation.Status.CHECK_IN]:
                raise ValidationError(
                    "この設問に紐づく予約に「予約」または「チェックイン」のものがあるため、"
                    "タイトルを変更できません。"
                )

