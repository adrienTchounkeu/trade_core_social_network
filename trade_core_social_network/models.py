from django.db import models


class User(models.Model):
    id = models.AutoField
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=512)
    geolocation_data_ip = models.GenericIPAddressField(blank=True, null=True)
    geolocation_data_country = models.CharField(max_length=200)
    holiday = models.CharField(max_length=300, blank=True, null=True)
    token = models.CharField(max_length=300)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        print(self.geolocation_data_ip)


class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    text = models.CharField(max_length=500, blank=False)
    date_creation = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    views = models.ManyToManyField(User, related_name='+', through='ViewPost')
    likes = models.ManyToManyField(User, related_name='+', through='LikePost')
    unlikes = models.ManyToManyField(User, related_name='+', through='UnLikePost')


class ViewPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_viewed = models.DateTimeField(auto_now_add=True)
    reason_viewed = models.CharField(max_length=100)


class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_liked = models.DateTimeField(auto_now_add=True)
    like_raison = models.CharField(max_length=100)


class UnLikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_unliked = models.DateTimeField(auto_now_add=True)
    unlike_raison = models.CharField(max_length=100)
