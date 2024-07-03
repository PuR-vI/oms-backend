from django.db import models

# Create your models here.


class User(models.Model):
    userId=models.AutoField(primary_key=True)
    firstName=models.CharField(max_length=100)
    lastName=models.CharField(max_length=100)
    employeeId=models.CharField(max_length=100,unique=True)
    email=models.CharField(max_length=100)
    role=models.CharField(max_length=100)
    

    