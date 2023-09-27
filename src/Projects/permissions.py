from rest_framework.permissions import BasePermission
from .models import Project, Contributor


class isAuthor(BasePermission):
    def has_permission(self, request, view):
        AUTHORIZED_METHODS = ["GET", "POST"]
        RESTRICTED_METHODS = ["PUT", "DELETE"]
        project_id = request.project
        contributor = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )[0]
        permission_level = contributor.permission

        if request.method in AUTHORIZED_METHODS:
            return True

        if request.method in RESTRICTED_METHODS:
            if permission_level == "isAuthor":
                return True

        return False


class isContributor(BasePermission):
    def has_permission(self, request, view):
        AUTHORIZED_METHODS = ["GET", "POST"]
        RESTRICTED_METHODS = ["PUT", "DELETE"]
        project_id = request.project
        contributor = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )[0]
        permission_level = contributor.permission

        if request.method in AUTHORIZED_METHODS:
            return True

        if request.method in RESTRICTED_METHODS:
            if permission_level == "isContributor":
                return True

        return False


class ProjectAccessPermission(BasePermission):
    def has_permission(self, request, view):
        CONTRIBUTOR_METHODS = ["GET", "POST"]
        AUTHOR_METHODS = ["PUT", "DELETE"]
        project_id = request.project
        contributor = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )[0]
        permission_level = contributor.permission

        if request.method in CONTRIBUTOR_METHODS:
            if permission_level in ["isAuthor", "isContributor"]:
                return True

        if request.method in AUTHOR_METHODS:
            if permission_level == "isAuthor":
                return True

        return False


class ContributorAccessPermission(BasePermission):
    def has_permission(self, request, view):
        CONTRIBUTOR_METHODS = [
            "GET",
        ]
        AUTHOR_METHODS = ["POST", "PUT", "DELETE"]
        project_id = request.project
        contributor = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )[0]
        permission_level = contributor.permission

        if request.method in CONTRIBUTOR_METHODS:
            if permission_level in ["isAuthor", "isContributor"]:
                return True

        if request.method in AUTHOR_METHODS:
            if permission_level == "isAuthor":
                return True

        return False

