from django.db import models


class Speaker(models.Model):
    telegram_id = models.CharField(max_length=15)
    block = models.CharField(max_length=255)
    time_gap = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Program(models.Model):
    top_block = models.CharField(max_length=255)
    bottom_block = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return self.bottom_block
