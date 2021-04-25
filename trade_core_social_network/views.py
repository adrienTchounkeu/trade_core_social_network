from trade_core_social_network.models import User, Post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserList(APIView):
    """
    Create and Retrieve a User
    """

    def post(self, request, format=None):
        return Response(request.data)

    def get(self, request, format=None):
        return Response(request.data)


class PostList(APIView):
    """
    Create and Retrieve a Post
    """

    def post(self, request, format=None):
        return Response(request.data)

    def get(self, request, format=None):
        return Response(request.data)


class LoginUser(APIView):
    """
    Login a User
    """

    def post(self, request, format=None):
        pass


class UserLikePost(APIView):
    """
    Like a post
    """

    def post(self, request, format=None):
        pass


class UserUnlikePost(APIView):
    """
    UnLike a post
    """

    def post(self, request, format=None):
        pass


class UserViewPost(APIView):
    """
    View a post
    """

    def post(self, request, format=None):
        pass
