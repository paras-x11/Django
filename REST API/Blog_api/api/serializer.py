from rest_framework import serializers
from api.models import *

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
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
        read_only_fields = ['author']

    def create(self, validated_data):
        # print(self.data, "\n", self.context)
        request = self.context.get('request')
        if request and request.user:
            validated_data['author'] = request.user
        else:
            raise serializers.ValidationError("user not found in context")
        return super().create(validated_data)

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['author'] = UserSerializer(instance.author).data
        return resp

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {
            'author': {'read_only': True},
            'blog': {'read_only': True},
        }
    
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['author'] = UserSerializer(instance.author).data
        resp['blog'] = BlogSerializer(instance.blog).data
        return resp
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
        extra_kwargs = {
            'blog': {'read_only': True},
            'user': {'read_only': True},
        }
    
    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['blog'] = BlogSerializer(instance.blog).data
        resp['user'] = UserSerializer(instance.user).data
        return resp 