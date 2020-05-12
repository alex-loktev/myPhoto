from django.views.generic import View
from django.http import JsonResponse, HttpResponseBadRequest
from .models import *


class PostDetail(View):
    def get(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        id = request.GET.get('id', None)
        post = Post.objects.get(id=id)
        if request.user == post.author:
            delete = True
        else:
            delete = False
        if request.user in post.users_like.all():
            action = "dislike"
        else:
            action = "like"
        return JsonResponse({'author': post.author.username,
                             'image': post.image.url,
                             'avatar': post.author.profile.avatar.url,
                             'description': post.description,
                             'likes': post.users_like.count(),
                             'id': post.id,
                             'action': action,
                             'delete': delete,
                             })

    def post(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        id = request.POST.get('id', None)
        if id:
            post = Post.objects.get(id=id)
            if request.user in post.users_like.all():
                post.users_like.remove(request.user)
                action = "dislike"
            else:
                post.users_like.add(request.user)
                action = "like"
        return JsonResponse({'likes': post.users_like.count(),
                             'action': action,
                             'id': id,
                             })
