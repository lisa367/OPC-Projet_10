from rest_framework.permissions import BasePermission
from .serializers import IssueSerializer, CommentSerializer
from Projects.models import Contributor
from .models import Issue, Comment


class canAccessIssues(BasePermission):
    def has_permission(self, request, view):
        AUTHORIZED_METHODS = ["GET", "POST"]
        RESTRICTED_METHODS = ["PUT", "DELETE"]
        project_id = request.query_params.get("project_id")
        issue_id = request.query_params.get("issue_id")
        
        

        is_project_member = Contributor.objects.filter(project=project_id, user=request.user)[0]
        issue_object = Issue.objects.filter(pk=issue_id)[0]
        # is_object_author = Issue.objects.filter(pk=issue_id, project=project_id, author_user_id=user_id)[0]

        if request.method in AUTHORIZED_METHODS:
            if is_project_member: 
                return True

        if request.method in RESTRICTED_METHODS:
            if issue_object.author_user_id == request.user:
                return True

        return False


class canAccessComments(BasePermission):
    def has_permission(self, request, view):
        AUTHORIZED_METHODS = ["GET", "POST"]
        RESTRICTED_METHODS = ["PUT", "DELETE"]
        """ project_id = request.project
        issue_id = request.issue_id """
        project_id = request.query_params.get("project_id")
        issue_id = request.query_params.get("issue_id")

        is_project_member = Contributor.objects.filter(project=project_id, user=request.user,)[0]
        issue_object = Issue.objects.filter(pk=issue_id)[0]
        # is_object_author = Issue.objects.filter(pk=issue_id, project=project_id, author_user_id=request.user)[0]

        if request.method in AUTHORIZED_METHODS:
            if is_project_member: 
                return True

        if request.method in RESTRICTED_METHODS:
            if issue_object.author_user_id == request.user:
                return True

        return False
    

