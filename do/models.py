from django.db import models
from django.contrib.auth.models import User


class todo(models.Model):
    title = models.CharField(max_length=100)
    discription = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    datecomplited = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title