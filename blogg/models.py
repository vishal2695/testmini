from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class blogg(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    brief = models.TextField(max_length=500)
    link = models.URLField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    dtn = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='like_blogg', blank=True)

    def total_likes(self):
        return self.likes.count()

class comment(models.Model):
    commentt = models.ForeignKey(blogg, on_delete=models.CASCADE)
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    dat = models.DateTimeField(auto_now_add=True)


class profile(models.Model):
    profile_id = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    dp = models.ImageField(null=True, blank=True, upload_to='profile_pics')

