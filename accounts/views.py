from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from posts.models import Post
from .forms import *
from .models import Profile
from django.urls import reverse


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'accounts/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.set_password(form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('account:login')
        return render(request, 'accounts/registration.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        posts = Post.objects.all().filter(author=user)
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})


class ProfileDetail(LoginRequiredMixin, View):
    def get(self, request, id):
        user = Profile.objects.get(id=id).user
        if request.user == user:
            return redirect('account:profile')
        posts = Post.objects.all().filter(author=user)
        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})


class SubscribeOrUnsibscribe(LoginRequiredMixin, View):
    def post(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        action = request.POST.get('action', None)
        print(action)
        id = request.POST.get('profile', None)
        profile = Profile.objects.get(id=id)
        if action == 'subscribe':
            profile.followers.add(request.user.profile)
            return JsonResponse({'action': 'unsubscribe'})
        elif action == 'unsubscribe':
            profile.followers.remove(request.user.profile)
            return JsonResponse({'action': 'subscribe'})


class SettingsView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['avatar', 'name', 'surname', 'description']
    template_name = 'accounts/settings.html'

    def get_success_url(self):
        return reverse('account:profile')


class NewsLineView(LoginRequiredMixin, View):
    def get(self, request):
        posts = Post.objects.exclude(author=request.user)
        profiles = request.user.profile.subs.values_list('user', flat=True)
        posts = posts.filter(author_id__in=profiles)
        paginator = Paginator(posts, 5)
        page = request.GET.get('page', )
        posts = paginator.get_page(page)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            posts = paginator.page(paginator.num_pages)
        if request.is_ajax():
            return render(request, 'accounts/includes/newsLine_ajax.html',
                          {'posts': posts})
        return render(request, 'accounts/newsLine.html', {'posts': posts})


class PostAddView(LoginRequiredMixin, FormView):
    form_class = PostAddForm
    template_name = 'accounts/postForm.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('account:profile')


class DeletePost(LoginRequiredMixin, View):
    def post(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        id = request.POST.get('id', None)
        post = Post.objects.get(id=id)
        if request.user == post.author:
            post.delete()
            return redirect('account:profile')
        return HttpResponseBadRequest()


class SearchUserView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.GET.get('inputSearch', None)
        users = User.objects.exclude(username=request.user.username).filter(username__startswith=username)
        return render(request, 'accounts/searchList.html', {'users': users})