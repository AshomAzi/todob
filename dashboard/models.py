from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()

    class Priority(models.TextChoices):
        Low =  "low","Low"
        Medium = "medium","Medium" 
        High = "high","High" 

    priority = models.CharField(max_length=10, 
                                choices=Priority.choices, 
                                default=Priority.Medium)
    def __str__(self):
        return self.title