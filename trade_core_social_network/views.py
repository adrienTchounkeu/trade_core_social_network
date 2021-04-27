from trade_core_social_network.models import User, Post, LikePost, UnLikePost, ViewPost
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
import requests
from celery import shared_task


class UserList(APIView):
    """
    Create and Retrieve a User
    """

    # create a user
    def post(self, request, format=None):
        data = request.data

        response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key={}&email={}"
                                .format(env('EMAIL_API_KEY'), data['email']))
        content = response.content
        if content['deliverability'] == 'DELIVERABLE':
            user = User()
            user.email = data['email']
            user.password = make_password(data['password'])
            user.save()
            data_enrichment(user.email)  # data enrichment
            return dict(status=status.HTTP_201_CREATED, message=f"{user.email} created successfully")
        else:
            return dict(status=status.HTTP_406_NOT_ACCEPTABLE,
                        message=f"{data['email']} is not a valid email")

    # get user data
    def get(self, request, format=None):
        email = request.data['email']
        user = User.objects.get(pk=email)
        return Response(user)


@shared_task
def data_enrichment(email):
    user = User.objects.get(pk=email)
    response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key={}"
                            .format(env('GEOLOCATION_API_KEY')))
    content = response.content
    ip_address = content['ip_address']
    country = content['country']
    user.geolocation_data_ip = ip_address
    user.geolocation_data_country = country

    country_code = content['country_code']
    from datetime import datetime
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year
    response = requests.get("https://holidays.abstractapi.com/v1/?api_key={}&country={}&year={}&month={}&day={}"
                            .format(env('HOLIDAY_API_KEY'), country_code, current_year, current_month, current_day))
    content = response.content
    if len(content) != 0:
        holiday = content[0]
        user.holiday = holiday.name
    user.save()


class PostList(APIView):
    """
    Create and Retrieve a Post
    """

    # create a post
    def post(self, request, format=None):
        data = request.data
        post = Post()
        post.text = data['text']
        user_creator = User.objects.get(pk=data['email'])
        post.creator = user_creator
        post.save()
        return Response("Succesfully created!")

    # get data of a post : input -> id of post
    def get(self, request, format=None):
        data = request.data
        post = Post.objects.get(pk=data['id_post'])
        # todo include serializers
        return Response(post)


class LoginUser(APIView):
    """
    Login a User
    """

    def post(self, request, format=None):
        data = request.data
        try:
            user = User.objects.get(data['email'])
            if check_password(data['password'], user.email):
                # todo give access token
                return Response("User successfully connect")
            return Response("Email or password incorrect", status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response("Email or password incorrect", status=status.HTTP_401_UNAUTHORIZED)


class UserLikePost(APIView):
    """
    Like a post
    """

    def post(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        likeship = LikePost()
        likeship.user = user
        likeship.post = post
        likeship.save()
        pass


class UserUnlikePost(APIView):
    """
    UnLike a post
    """

    def post(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        unlikeship = UnLikePost()
        unlikeship.user = user
        unlikeship.post = post
        unlikeship.save()
        pass


class UserViewPost(APIView):
    """
    View a post
    """

    def post(self, request, format=None):
        data = request.data
        user = User.objects.get(pk=data['email'])
        post = Post.objects.get(pk=data['id_post'])
        viewship = ViewPost()
        viewship.user = user
        viewship.post = post
        viewship.save()
        pass
