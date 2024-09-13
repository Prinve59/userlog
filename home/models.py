from django.db import models

# Create your models here.
class Contact(models.Model):
    username=models.CharField( max_length=10)
    cpassword=models.CharField(max_length=50)

def __str__(self):
    return self.name