from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    email =models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.name