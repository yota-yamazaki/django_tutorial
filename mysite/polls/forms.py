from django import forms
from . import models

class ChoiceAdminForm(forms.ModelForm):
    def clean_choice_text(self):
        choice_text = self.cleaned_data['choice_text']
        if "hoge" in choice_text:
            raise forms.ValidationError("テキストにはhogeを入れない！")
        return choice_text

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ["question_text"]

class QuestionEditForm(QuestionForm):
    pass
