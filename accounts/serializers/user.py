from rest_framework import serializers
from accounts.models import User
from gallery.serializers import PictureSerializer


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    email = serializers.EmailField(required=False)

    avatar = serializers.ImageField(required=False)

    pictures = PictureSerializer(required=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'pictures']
