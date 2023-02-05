from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, max_length=68, min_length=8)


class LoginSerializerResopnse(serializers.Serializer):
    refresh = serializers.CharField(max_length=200)
    access = serializers.CharField(max_length=200)
