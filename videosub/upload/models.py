from django.db import models

# Create your models here.

class Video(models.Model):
    name = models.CharField(max_length=30)
    video = models.FileField(upload_to='media/')

class Subtitles(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    subtitle = models.FileField(upload_to='media/')
