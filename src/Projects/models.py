from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=250)
    type = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)


class Contributor(models.Model):
    PERMISSIONS = [
        ("isAuthor", "isAuthor"),
        ("isContributor", "isContributor"),
    ]

    user = models.ManyToManyField(User)
    project = models.ManyToManyField(Project)
    permission = models.CharField(max_length=120, choices=PERMISSIONS)
    role = models.CharField(max_length=120)
