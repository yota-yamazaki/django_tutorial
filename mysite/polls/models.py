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
    class Meta:
        ordering = ['position']
        verbose_name = verbose_name_plural = '選択肢'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    position = models.PositiveSmallIntegerField("Position", null=True)

    def __str__(self):
        return self.choice_text

class Reservation(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '予約'

    class Status(models.TextChoices):
        RESERVED = '予約', '予約'
        CHECK_IN = 'チェックイン', 'チェックイン'
        COMPLETED = '完了', '完了'
        CANCEL = 'キャンセル', 'キャンセル'
        CANCEL_NOT_CHECK_IN = 'ドタキャン', 'ドタキャン'

    reservation_number = models.CharField(max_length=255, verbose_name="予約番号")
    status = models.TextField(max_length=255, choices=Status, verbose_name="ステータス")
    
    def __str__(self):
        return self.reservation_number

