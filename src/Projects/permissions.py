from rest_framework.permissions import BasePermission
from .models import Project, Contributor


class ProjectAccessPermission(BasePermission):
    def has_permission(self, request, view, *args, **kwargs):
        ANY_USER_METHODS = ["POST"]
        MEMBER_ONLY_METHODS = ["GET",]
        AUTHOR_ONLY_METHODS = ["PUT", "DELETE"]
        project_id = request.resolver_match.kwargs.get("project_id")
        # print(project_id)
        contributor_query = Contributor.objects.filter(project=project_id, user=request.user,)

        if request.method in ANY_USER_METHODS:
                return True

        if contributor_query:
            contributor = contributor_query[0]
            permission_level = contributor.permission


            if request.method in MEMBER_ONLY_METHODS:
                if permission_level in ["isAuthor", "isContributor"]:
                    return True

            if request.method in AUTHOR_ONLY_METHODS:
                if permission_level == "isAuthor":
                    return True

        return False


class ContributorAccessPermission(BasePermission):
    def has_permission(self, request, view):
        MEMBER_ONLY_METHODS = ["GET",]
        AUTHOR_ONLY_METHODS = ["POST", "PUT", "DELETE"]
        project_id = request.resolver_match.kwargs.get("project_id")
        print(f"{project_id}")
        contributor_query = Contributor.objects.filter(project=project_id, user=request.user,)
        if contributor_query:
            contributor = contributor_query[0]
            permission_level = contributor.permission
            print(permission_level)

            if request.method in MEMBER_ONLY_METHODS:
                if permission_level in ["isAuthor", "isContributor"]:
                    print("MEMBER_ONLY_METHODS")
                    return True

            if request.method in AUTHOR_ONLY_METHODS:
                if permission_level == "isAuthor":
                    print("AUTHOR_ONLY_METHODS")
                    return True

        return False

