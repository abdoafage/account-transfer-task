from django.db import models

# Create your models here.

class Account(models.Model):
    account_id = models.CharField(max_length=255, unique=True, auto_created=True, primary_key=True)
    name = models.CharField(max_length=255)
    balance = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
