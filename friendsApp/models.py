from django.db import models

# Create your models here.


class Friends(models.Model):
  title = models.CharField(max_length=100)
  # scene = models.CharField(max_length=500,null=True,blank=True)
  character = models.CharField(max_length=20)
  text = models.CharField(max_length=1000)
  season = models.CharField(max_length=100)
  episode = models.CharField(max_length=100)
  relevancy = models.IntegerField()
  # level = models.CharField(max_length=300,choices=CHOICES)

  def __str__(self):
    return self.text
