"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from Projects.views import (
    ProjectListView,
    ProjectDetailView,
    ContributorListView,
    ContributorDetailView,
)
from Issues.views import (
    IssueListView,
    IssueDetailView,
    CommentListView,
    CommentDetailView,
)

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path("", include("rest_framework.urls")),
    path("", include("Accounts.urls")),
    path("projects/", ProjectListView.as_view()),
    path("projects/<int:project_id>", ProjectDetailView.as_view()),
    path("projects/<int:project_id>/users", ContributorListView.as_view()),
    path("projects/<int:project_id>/users/<int:user_id>", ContributorDetailView.as_view()),
    path("projects/<int:project_id>/issues", IssueListView.as_view()),
    path("projects/<int:project_id>/issues/<int:issue_id>", IssueDetailView.as_view()),
    path("projects/<int:project_id>/issues/<int:issue_id>/comments", CommentListView.as_view()),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>",
        CommentDetailView.as_view(),
    ),
]
