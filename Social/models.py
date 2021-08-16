from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
import cloudinary
class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, blank=True)
    body = models.TextField(blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')


    class Meta:
        verbose_name = 'Posts'
        verbose_name_plural = 'Posts'


class Profile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = CloudinaryField('image', null=True)
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    location = models.CharField(blank=True, max_length=100, null=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    


@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender= User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(pre_delete, sender = Posts)
def post_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)

@receiver(pre_delete, sender = Profile)
def profile_delete(sender, instance, **kwargs):
    cloudinary.uploader.destroy(instance.image.public_id)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    comment = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)