from django.db import models


class Speaker(models.Model):
    telegram_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    speech_theme = models.CharField(max_length=255)
    speech_begin_time = models.DateTimeField()
    speech_end_time = models.DateTimeField()
