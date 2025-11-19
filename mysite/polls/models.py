import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):

    class Meta:
        verbose_name = verbose_name_plural = '設問'


    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    position = models.PositiveSmallIntegerField("Position", null=True)

    class Meta:
        ordering = ['position']
        verbose_name = verbose_name_plural = '選択肢'
    def __str__(self):
        return self.choice_text
