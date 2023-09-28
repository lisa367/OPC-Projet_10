from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.http import QueryDict

from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import ProjectAccessPermission, ContributorAccessPermission


class ProjectListView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs,):
        user_projects = Contributor.objects.filter(user=request.user)
        projects_id_list = [obj.project.all()[0].id for obj in user_projects]
        print(projects_id_list)
        projects = Project.objects.filter(pk__in=projects_id_list)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Setting the permission level for the creator of the project
            new_pk = serializer.data["id"]
            role = serializer.data.get("role", "Project manager")

            new_contributor = {
                "user": str(request.user.id),
                "project": str(new_pk),
                "permission": "isAuthor",
                "role": role,
            }
            query_dict = QueryDict("", mutable=True)
            query_dict.update(new_contributor)
            project_author = ContributorSerializer(data=query_dict)

            if project_author.is_valid():
                project_author.save()
            else:
                print(f"Serializer not valid : {project_author}")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, ProjectAccessPermission]

    def get_object(self, project_id):
        try:
            return Project.objects.filter(pk=project_id)[0]
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, project_id, format=None):
        project = self.get_object(project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, project_id, format=None):
        project = self.get_object(project_id)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, format=None):
        project = self.get_object(project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorListView(APIView):
    permission_classes = [IsAuthenticated, ContributorAccessPermission]

    def get(self, request, project_id, *args, **kwargs):
        contributors = Contributor.objects.filter(project=project_id)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorDetailView(APIView):
    permission_classes = [IsAuthenticated, ContributorAccessPermission]

    def get_object(self, project_id, user_id):
        try:
            contributor = Contributor.objects.filter(project=project_id, user=user_id)[
                0
            ]
            print(type(contributor))
            return contributor
        except Contributor.DoesNotExist:
            raise Http404

    def get(self, request, project_id, user_id, format=None):
        contributor = self.get_object(project_id, user_id)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data)

    def put(self, request, project_id, user_id, format=None):
        contributor = self.get_object(project_id, user_id)
        if contributor:
            serializer = ContributorSerializer(contributor, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response("That contributor does not exists. Please check the data you provided.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self, request, project_id, user_id, format=None):
        contributor = self.get_object(
            project_id,
            user_id,
        )
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
