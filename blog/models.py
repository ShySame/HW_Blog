from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=300)
    text = models.TextField(max_length=3500)
    description = models.TextField(max_length=1000, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    img = models.URLField()
    published=models.BooleanField(default=True)

    def __str__(self):
        return f'{" ".join(self.title.split()[:3])}...'


class Comment(models.Model):
    username=models.CharField(max_length=100)
    text=models.TextField(max_length=1000)
    is_published = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.username}-{" ".join(self.text.split()[:3])}...'
