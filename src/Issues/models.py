from django.db import models
from django.contrib.auth import get_user_model

from Projects.models import Project

User = get_user_model()


class Issue(models.Model):
    title = models.CharField(max_length=120)
    desc = models.CharField(max_length=120)
    tag = models.CharField(max_length=120)
    priority = models.CharField(max_length=120)
    # project_id = models.IntegerField()
    project_id = models.ForeignKey(to=Project, on_delete=models.SET_DEFAULT, default=0)
    status = models.CharField(max_length=120)
    author_user_id = models.ForeignKey(
        User, related_name="author_id", on_delete=models.SET_DEFAULT, default=0
    )
    assignee_user_id = models.ForeignKey(
        User, related_name="assignee_id", on_delete=models.SET_DEFAULT, default=0
    )
    created_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    description = models.CharField(max_length=120)
    author_user_id = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=0)
    issue_id = models.ForeignKey(Issue, on_delete=models.SET_DEFAULT, default=0)
    created_time = models.DateTimeField(auto_now=True)
