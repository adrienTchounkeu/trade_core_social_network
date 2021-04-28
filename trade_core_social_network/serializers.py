from rest_framework import serializers
from .models import User, Post, LikePost, UnLikePost, ViewPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = '__all__'


class UnLikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnLikePost
        fields = '__all__'


class ViewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewPost
        fields = '__all__'
