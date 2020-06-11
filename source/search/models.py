from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from event.models import Event
# Create your models here.

# class Category(models.Model):
#     caption = models.CharField(max_length=16)

# class ArticleType(models.Model):
#     caption = models.CharField(max_length=16)

# class Article(models.Model):
#     title = models.CharField(max_length=32)
#     content = models.CharField(max_length=255)

#     category = models.ForeignKey(to='Category',on_delete=models.CASCADE)
#     article_type = models.ForeignKey(to='ArticleType',on_delete=models.CASCADE)

#     # type_choice = (
#     #     (0,'Python'),
#     #     (1,'OpenStack'),
#     #     (2,'Linux'),
#     # )
#     # article_type_id = models.IntegerField(choices=type_choice)