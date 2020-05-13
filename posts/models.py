from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class Post(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    description = models.TextField(blank=True, null=True)
    users_like = models.ManyToManyField(User, related_name='images_liked', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = '{}_{}'.format(self.author, timezone.now())
            self.slug = slugify(slug)
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)