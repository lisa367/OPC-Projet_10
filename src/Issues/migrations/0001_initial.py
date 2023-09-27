# Generated by Django 4.2.4 on 2023-08-28 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Projects', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('desc', models.CharField(max_length=120)),
                ('tag', models.CharField(max_length=120)),
                ('priority', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=120)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('assignee_user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='assignee_id', to=settings.AUTH_USER_MODEL)),
                ('author_user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='author_id', to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='Projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=120)),
                ('created_time', models.DateTimeField(auto_now=True)),
                ('author_user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
                ('issue_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='Issues.issue')),
            ],
        ),
    ]
