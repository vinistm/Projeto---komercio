from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','username','password','first_name','last_name','city','date_joined','is_superuser','is_active']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ["is_active",'date_joined','is_superuser']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class DetailUserSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['id','username','first_name', 'last_name', 'is_seller', 'date_joined','is_active','is_superuser']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

class UpdateStatusSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['is_active']
