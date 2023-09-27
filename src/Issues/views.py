from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from Projects.models import Contributor
from .models import Issue, Comment
from .serializers import IssueSerializer, CommentSerializer
from .permissions import canAccessIssues, canAccessComments


# Create your views here.
class IssueListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, *args, **kwargs):
        issues = Issue.objects.filter(project_id=project_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, issue_id):
        try:
            return Issue.objects.filter(pk=issue_id)[0]
        except Issue.DoesNotExist:
            raise Http404

    def get(self, request, project_id, issue_id):
        issue = self.get_object(issue_id)
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    def put(self, request, project_id, issue_id):
        issue = self.get_object(issue_id)
        # print(issue.assignee_user_id)
        serializer = IssueSerializer(issue, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """ for key in request.data:
            if key.isdigit():
                new_data = request.data[int(key)]
            else:
                new_data = request.data[key]

            try:
                setattr(issue, key, new_data)
                issue.save()
                print(issue.assignee_user_id)

            except KeyError:
                return Response(
                    f"KeyError, please check your parameters : {request.data}"
                )
            return Response(request.data) """

    def delete(self, request, project_id, issue_id):
        issue = self.get_object(issue_id)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id, issue_id, *args, **kwargs):
        comments = Comment.objects.filter(issue_id=issue_id)
        #comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, comment_id):
        try:
            return Comment.objects.filter(pk=comment_id)[0]
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, project_id, issue_id, comment_id, format=None):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, project_id, issue_id, comment_id, format=None):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        """ for key in request.data:
            new_data = request.data[key]
            try:
                # contributor[key] =
                setattr(comment, key, new_data)
                comment.save()
                # print(contributor[key])
            except KeyError:
                pass 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
        

    def delete(self, request, project_id, issue_id, comment_id, format=None):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
