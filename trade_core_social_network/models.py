from django.db import models
import requests


class User(models.Model):
    email = models.EmailField(primary_key=True)
    geolocation_data = models.IPAddressField()
    holiday = models.JSONField(blank=True, null=True)
    token = models.CharField(max_length=300)

    # add the email validation before saving users
    def save(self, *args, **kwargs):
        # verify the email
        
        super().save(self, *args, **kwargs)


class Post(models.Model):
    id_post = models.CharField(max_length=100, primary_key=True)
    text = models.CharField(max_length=500)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.ManyToManyField(User, through='ViewPost')
    likes = models.ManyToManyField(User, through='LikePost')
    unlikes = models.ManyToManyField(User, through='UnLikePost')


class ViewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_viewed = models.DateTimeField()
    reason_viewed = models.CharField(max_length=100)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateTimeField()
    like_raison = models.CharField(max_length=100)


class UnLikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_unliked = models.DateTimeField()
    unlike_raison = models.CharField(max_length=100)
