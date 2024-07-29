from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(primary_key=True, blank=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    POST_TYPES = [('c', 'copyright'), ('p', 'public content')]

    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=1, choices=POST_TYPES)
    image = models.ImageField(upload_to='uploads')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    



