import json
from dataclasses import asdict

from rest_framework import serializers

from tasks.models import Task


class AuthLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AuthChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'execution_at', 'is_done']
        read_only_fields = fields


class RetrieveTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'execution_at', 'is_done']
        read_only_fields = fields


class CreateOrUpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'execution_at', 'is_done']
        read_only_fields = ['id', 'is_done']
