from logging import getLogger

from django.db import connections
from django.db.utils import OperationalError
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from tasks.models import Task
from tasks.utils import ActionSerializerViewSetMixin
from tasks import actions
from tasks import serializers


logger = getLogger('django')


class HealthViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []
    pagination_class = None

    @action(methods=['GET'], detail=False, url_path='alive')
    def alive(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='ready')
    def ready(self, request, *args, **kwargs):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
        except OperationalError:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            c.close()
            return Response(status=status.HTTP_200_OK)


class ToDoViewSet(ActionSerializerViewSetMixin,
                  mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_classes = {
        'list': serializers.ListTaskSerializer,
        'retrieve': serializers.RetrieveTaskSerializer,
        ('create', 'update', 'partial_update'): serializers.CreateOrUpdateTaskSerializer
    }

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        if self.action == 'list':
            qs = qs.defer('description')
        return qs

    def create(self, request, *args, **kwargs):
        logger.info(f'create task title={request.data["title"]}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk: int = None, *args, **kwargs):
        logger.info(f'update task with id={pk}')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, pk: int = None, *args, **kwargs):
        logger.info(f'destroy task with id={pk}')
        return super().destroy(request, *args, **kwargs)

    @action(methods=['POST'], detail=True)
    def execute(self, request, pk: int = None, *args, **kwargs):
        logger.info(f'execute task with id={pk}')
        actions.ExecuteTask()(pk)
        return Response(status=status.HTTP_200_OK)


class AuthViewSet(ActionSerializerViewSetMixin,
                  viewsets.GenericViewSet):
    serializer_classes = {
        'login': serializers.AuthLoginSerializer,
        'change_password': serializers.AuthChangePasswordSerializer
    }

    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        logger.info('log in user')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = actions.AuthLogin()(**serializer.validated_data)
        return Response({'token': token}, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def logout(self, request, *args, **kwargs):
        logger.info('log out user')
        actions.AuthLogout()(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=(IsAuthenticated,))
    def change_password(self, request, *args, **kwargs):
        logger.info('change password user')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        actions.AuthChangePassword()(user=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
