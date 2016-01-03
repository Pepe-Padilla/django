
#
# from django.shortcuts import get_object_or_404

from users.models import UserDetail
from users.serializers import UserSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from oauth2_provider.ext.rest_framework import OAuth2Authentication, TokenHasScope


class UserViewSet(GenericViewSet):

    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['write']

    queryset = UserDetail.objects.all()
    serializer_class = UserSerializer

    def list(self, request):

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_paginated_response(self, data):

        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def create(self, request):

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk):
        user = get_object_or_404(UserDetail, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user)
        serialized_user = serializer.data

        return Response(serialized_user)

    def update(self, request, pk):
        user = get_object_or_404(UserDetail, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        user = get_object_or_404(UserDetail, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        return UserSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)