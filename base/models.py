from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Priority(models.Model):
    LEVEL_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.level
    
class Task(models.Model):
    title = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=1000, null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


