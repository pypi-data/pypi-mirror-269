from django.db import models


class App(models.Model):
    id = models.CharField(unique=True, primary_key=True, max_length=50)
    secret = models.CharField(max_length=50)
    signing_secret = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=100)
