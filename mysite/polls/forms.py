from dataclasses import fields
from django import forms
from . import models

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

    class Meta:
        fields = ["choice_text", "question"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ["question_text",]

class QuestionEditForm(QuestionForm):
    pass

    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        if "piyo" in question_text:
            raise forms.ValidationError("テキストにはpiyoを入れないでください")
        return question_text

class QuestionAdminForm(QuestionForm):
    pass

    def clean_question_text(self):
        question_text = self.cleaned_data['question_text']
        if "piyo" in question_text:
            raise forms.ValidationError("テキストにはpiyoを入れないでください")
        return question_text
