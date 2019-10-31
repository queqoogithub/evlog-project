from django.db import models
from datetime import datetime

# Create your models here.

class Post(models.Model):
    # Fields
    title = models.CharField(max_length=200)
    title_image = models.ImageField(upload_to='blog_title_image/', null=True, blank=True)
    author = models.ForeignKey( 'auth.User', on_delete=models.CASCADE, )
    date = models.DateTimeField('date published', default=datetime.now)
    text = models.TextField() 
    # Metadata
    class Meta:
        ordering = ['-date'] # To order the QuerySet.
    # Methods
    def __str__(self):
        return self.title

class About(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title
