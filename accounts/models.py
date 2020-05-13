from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    default_avatar = models.ImageField(default='avatars/default.jpg')
    name = models.CharField(max_length=40, blank=True)
    surname = models.CharField(max_length=40, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=300, blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name='subs', symmetrical=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('account:profile')