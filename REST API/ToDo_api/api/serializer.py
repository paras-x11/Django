from rest_framework import serializers  
from api.models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("User not found in context.")
        return super().create(validated_data)

    def to_representation(self, instance):
        # print("Instance in to_representation:", instance)  # Debug: Check instance
        resp = super().to_representation(instance)
        resp['user'] = UserSerializer(instance.user).data
        # print("Serialized Response:", resp)  # Debug: Output serialized data
        return resp
