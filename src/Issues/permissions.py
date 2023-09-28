from rest_framework.permissions import BasePermission
from .serializers import IssueSerializer, CommentSerializer
from Projects.models import Contributor
from .models import Issue, Comment


class canAccessIssues(BasePermission):
    def has_permission(self, request, view):
        MEMBER_ONLY_METHODS = ["GET", "POST"]
        AUTHOR_ONLY_METHODS = ["PUT", "DELETE"]
        project_id = request.resolver_match.kwargs.get("project_id")
        issue_id = request.resolver_match.kwargs.get("issue_id")
        

        is_project_member = Contributor.objects.filter(project=project_id, user=request.user)
        issue_object = Issue.objects.filter(pk=issue_id)
        # is_object_author = Issue.objects.filter(pk=issue_id, project=project_id, author_user_id=user_id)[0]


        if request.method in MEMBER_ONLY_METHODS:
            if is_project_member: 
                return True

        if request.method in AUTHOR_ONLY_METHODS:
            if issue_object[0].author_user_id == request.user:
                return True

        return False


class canAccessComments(BasePermission):
    def has_permission(self, request, view):
        MEMBER_ONLY_METHODS = ["GET", "POST"]
        AUTHOR_ONLY_METHODS = ["PUT", "DELETE"]
        """ project_id = request.project
        issue_id = request.issue_id """
        project_id = request.resolver_match.kwargs.get("project_id")
        issue_id = request.resolver_match.kwargs.get("issue_id")

        is_project_member = Contributor.objects.filter(project=project_id, user=request.user,)
        comment_object = Comment.objects.filter(pk=issue_id)
        # is_object_author = Issue.objects.filter(pk=issue_id, project=project_id, author_user_id=request.user)[0]

        if request.method in MEMBER_ONLY_METHODS:
            if is_project_member: 
                return True

        if request.method in AUTHOR_ONLY_METHODS:
            if comment_object[0].author_user_id == request.user:
                return True

        return False
    

