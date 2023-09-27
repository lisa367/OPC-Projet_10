from rest_framework.permissions import BasePermission
from .models import Project, Contributor


class ProjectAccessPermission(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        CONTRIBUTOR_METHODS = ["GET", "POST"]
        AUTHOR_METHODS = ["PUT", "DELETE"]
        project_id = request.resolver_match.kwargs.get("project_id")
        print(project_id)
        contributor_query = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )
        if contributor_query:
            contributor = contributor_query[0]
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
        project_id = request.resolver_match.kwargs.get("project_id")
        print(project_id)
        contributor_query = Contributor.objects.filter(
            project=project_id,
            user=request.user,
        )
        if contributor_query:
            contributor = contributor_query[0]
            permission_level = contributor.permission

            if request.method in CONTRIBUTOR_METHODS:
                if permission_level in ["isAuthor", "isContributor"]:
                    return True

            if request.method in AUTHOR_METHODS:
                if permission_level == "isAuthor":
                    return True

        return False

