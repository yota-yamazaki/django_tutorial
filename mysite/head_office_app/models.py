from django.db import models

# Create your models here.

class Store(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '店舗'

    name = models.CharField(max_length=1024, verbose_name="店舗名")
    area = models.CharField(max_length=255, null=True, blank=True, verbose_name="地域")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class News(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = 'お知らせ'

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, verbose_name="タイトル")
    content = models.TextField(null=True, blank=True, verbose_name="内容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

