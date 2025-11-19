from dataclasses import fields
from django import forms
from . import models

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ["choice_text", "question"]

class ChoiceAdminForm(ChoiceForm):
    pass

    def clean_choice_text(self):
        choice_text = self.cleaned_data['choice_text']
        if "piyo" in choice_text:
            raise forms.ValidationError("テキストにはpiyoを入れないでください")
        return choice_text

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ["question_text"]

class QuestionEditForm(QuestionForm):
    pass

