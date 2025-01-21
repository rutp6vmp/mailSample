from django.db import models

# Create your models here.
from django.db import models

class Mail(models.Model):
    if_anonymous = models.IntegerField()  # 0: 匿名, 1: 不匿名
    text = models.TextField()
    user_name = models.CharField(max_length=255, blank=True, null=True)
    url_before = models.URLField()
    qr_width = models.IntegerField(default=300)
    qr_height = models.IntegerField(default=300)
    uuid = models.UUIDField(unique=True, editable=False, null=False)
    create_time = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    mail = models.OneToOneField(Mail, on_delete=models.CASCADE, related_name='feedback')
    answer = models.TextField()
    answer_time = models.DateTimeField(auto_now_add=True)
    live_time = models.DateTimeField(blank=True, null=True)
    is_answered = models.IntegerField()  # 0: 未讀, 1: 已回答, 2: 已閱
