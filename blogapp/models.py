from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE)



