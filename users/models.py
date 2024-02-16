from django.db import models
from datetime import datetime
from django.utils import timezone
import os, random
from django.utils.html import mark_safe

# Create your models here.

now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'profile_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance, basename = basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('&d'))

class User(models.Model):
    user_fname = models.CharField(max_length=200, verbose_name='First Name')
    user_lname = models.CharField(max_length=200, verbose_name='Last Name')
    user_email = models.EmailField(unique=True, max_length=200, verbose_name='Email')
    user_position = models.CharField(max_length=200, verbose_name='Position')
    user_username = models.CharField(max_length=100, verbose_name='Username')
    user_password = models.CharField(max_length=150, verbose_name='Password')
    user_image = models.ImageField(upload_to=image_path, default='profile_pic/image.jpg')

    def image_tag(self):
        return mark_safe('<img src="/users/media/%s" width="50" height="50" />' %(self.user_image))


    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user_email

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField(default='null')
    body = models.TextField(default='null')
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_time']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

