from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

"""create book catalog models for sqlite3 database"""

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    review = models.TextField()
    rating = models.IntegerField()
    genre = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    favorite = models.IntegerField()

    def __str__(self):
        return self.title
    
    
