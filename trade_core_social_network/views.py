from trade_core_social_network.models import User, Post, LikePost, UnLikePost, ViewPost
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password, make_password
import requests
from .celery_tasks import data_enrichment
from .settings import env
import json
from .serializers import UserSerializer, PostSerializer, LikePostSerializer, UnLikePostSerializer, ViewPostSerializer


class UserList(viewsets.ViewSet):
    """
    Create and Retrieve a User
    """

    # create a user
    def create(self, request, format=None):
        data = request.data

        response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key={}&email={}"
                                .format(env('EMAIL_API_KEY'), data['email']))
        content = json.loads(response.content)
        if content['deliverability'] == 'DELIVERABLE':
            user = User()
            user.email = data['email']
            user.password = make_password(data['password'])
            user.save()
            data_enrichment(user.email)  # data enrichment
            print("Data enrichment -- test")
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(f"{data['email']} is not a valid email", status=status.HTTP_406_NOT_ACCEPTABLE)

    # get user data
    def retrieve(self, request, pk=None):
        email = request.data['email']
        user = User.objects.get(pk=email)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostList(viewsets.ViewSet):
    """
    Create and Retrieve a Post
    """

    permissions_classes = (IsAuthenticated,)

    # create a post
    def create(self, request, format=None):
        data = request.data
        post = Post()
        post.text = data['text']
        user_creator = User.objects.get(pk=data['email'])
        post.creator = user_creator
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # get data of a post : input -> id of post
    def retrieve(self, request, pk=None):
        data = request.data
        post = Post.objects.get(pk=data['id_post'])
        serializer = PostSerializer(Post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginUser(viewsets.ViewSet):
    """
    Login a User
    """

    def retrieve(self, request, format=None):
        data = request.data
        try:
            user = User.objects.get(data['email'])
            if check_password(data['password'], user.email):
                # todo give access token
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response("Email or password incorrect", status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response("Email or password incorrect", status=status.HTTP_401_UNAUTHORIZED)


class UserLikePost(viewsets.ViewSet):
    """
    Like a post
    """

    permissions_classes = (IsAuthenticated,)

    def retrieve(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        likeship = LikePost()
        likeship.user = user
        likeship.post = post
        likeship.save()
        serializer = LikePostSerializer(likeship)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUnlikePost(viewsets.ViewSet):
    """
    UnLike a post
    """

    permissions_classes = (IsAuthenticated,)

    def retrieve(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        unlikeship = UnLikePost()
        unlikeship.user = user
        unlikeship.post = post
        unlikeship.save()
        serializer = UnLikePostSerializer(unlikeship)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewPost(viewsets.ViewSet):
    """
    View a post
    """

    permissions_classes = (IsAuthenticated,)

    def retrieve(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        viewship = ViewPost()
        viewship.user = user
        viewship.post = post
        viewship.save()
        serializer = ViewPostSerializer(viewship)
        return Response(serializer.data, status=status.HTTP_200_OK)
