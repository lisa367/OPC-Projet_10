from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.http import QueryDict

# from Accounts.models import CustomUserModel
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from .permissions import ProjectAccessPermission, ContributorAccessPermission


# Create your views here.
class ProjectListView(APIView):
    # permission_classes = [isAuthenticated, isAuthor, isContributor]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):
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
            # print(f"Raw data : {serializer.data}")
            # print(f"Validated data : {serializer.validated_data}")
            new_pk = serializer.data["id"]
            role = serializer.data.get("role", "Project manager")
            # print(f"{new_pk}")
            # print(role)

            # Setting the permission level for the creator of the project
            new_contributor = {
                "user": str(request.user.id),
                "project": str(new_pk),
                "permission": "isAuthor",
                "role": role,
            }
            query_dict = QueryDict("", mutable=True)
            query_dict.update(new_contributor)
            project_author = ContributorSerializer(data=query_dict)
            # print(project_author)
            if project_author.is_valid():
                # print(project_author)
                project_author.save()
            else:
                print(f"Serializer not valid : {project_author}")

            # project_author = Contributor.objects.create(user=request.user, project=new_pk, permission="isAuthor", role=role)
            """ project_author = Contributor.objects.filter(user=request.user, project=serializer.data.id)
            project_author.permission = "isAuthor"
            project_author.save() """
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response(request.user.id)


class ProjectDetailView(APIView):
    # permission_classes = [IsAuthenticated, isAuthor]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self, project_id):
        try:
            # return Project.objects.get(pk=pk)
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
        """serializer = ProjectSerializer(project, data=request.data) 
        for key in request.data:
            new_data = request.data[key]
            try:
                setattr(project, key, new_data)
                project.save()
                # project[key] = new_data
                # project.save()
            except KeyError:
                return Response(f"KeyError, please check your entry data: {request.data}")

        return Response(request.data) """

    def delete(self, request, project_id, format=None):
        project = self.get_object(project_id)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorListView(APIView):
    # permission_classes = [IsAuthenticated, isAuthor]
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, project_id, *args, **kwargs):
       # return Response("Done")
       # contributors = Contributor.objects.all()
        contributors = Contributor.objects.filter(project=project_id)
        # print(contributors)
        serializer = ContributorSerializer(contributors, many=True)
        # print(serializer)
        return Response(serializer.data)

    def post(self, request, project_id, *args, **kwargs):
        serializer = ContributorSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorDetailView(APIView):
    # permission_classes = [isAuthenticated, isAuthor]
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self, project_id, user_id):
        try:
            # return Contributor.objects.get(pk=pk)
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
            # return Response(serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response("That contributor does not exists. Please check the data you provided.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # contributor.permission = request.data["permission"]
        """ contributor.role = request.data["role"]
        contributor.save() """

        """ for key in request.data:
            new_data = request.data[key]
            try:
                # contributor[key] =
                setattr(contributor, key, new_data)
                contributor.save()
                # print(contributor[key])
            except KeyError:
                pass

        # print(contributor.role)
        return Response(f"{request.data}") """
        

    def delete(self, request, project_id, user_id, format=None):
        contributor = self.get_object(
            project_id,
            user_id,
        )
        contributor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
