from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from Social_media.forms import PostForm
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.contrib.auth import login
from .models import Post, Comment
from django.http import JsonResponse
from .forms import RegisterForm
from .models import Profile
from .forms import UserUpdateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin





def add_friend(request, username):
    if request.user.is_authenticated:
        other_user = get_object_or_404(User, username=username)
        request.user.profile.friends.add(other_user.profile)
    return redirect('user_profile', username=username)


def remove_friend(request, username):
    if request.user.is_authenticated:
        other_user = get_object_or_404(User, username=username)
        request.user.profile.friends.remove(other_user.profile)
    return redirect('user_profile', username=username)


def search_users(request):
    query = request.GET.get('q', '')
    users = []
    if query:
        users = User.objects.filter(username__icontains=query)
    return render(request, 'search.html', {'users': users, 'query': query})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            profile.save()
            login(request, user)
            return redirect(reverse('home'))
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST' and request.user == post.author:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user and request.method == 'POST':
        new_content = request.POST.get('comment_text')
        if new_content:
            comment.content = new_content
            comment.save()
            
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def share_post(request, pk):
    if request.user.is_authenticated:
        original_post = get_object_or_404(Post, pk=pk)
        
        if original_post.author == request.user:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
        Post.objects.create(
            author=request.user,
            content=original_post.content,
            image=original_post.image,
            shared_from=original_post
        )
        
    return HttpResponseRedirect(reverse('home'))


def add_comment(request, pk):
    if request.method == "POST" and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=comment_text
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'author': request.user.username,
                    'content': comment.content,
                    'comment_id': comment.id
                })
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            return redirect(reverse('home')) 
    else:
        form = PostForm()

    posts = Post.objects.all().select_related('author', 'author__profile', 'shared_from__author', 'shared_from__author__profile').prefetch_related('likes', 'comments__author').order_by('-created_at')
    return render(request, 'home.html', {'posts': posts, 'form': form})



def contacts(request):
    return render(request, 'contacts.html')

def post_list(request):
    posts = Post.objects.filter(published=True).select_related('author', 'author__profile', 'shared_from__author', 'shared_from__author__profile').prefetch_related('likes', 'comments__author').order_by('-created_at')
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, published=True)
    return render(request, 'post_detail.html', {'post': post})

def user_profile(request, username):
    profile_user_obj = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('user_profile', username=username)
    else:
        form = PostForm()

    posts = Post.objects.filter(author=profile_user_obj).select_related('author', 'author__profile', 'shared_from__author', 'shared_from__author__profile').prefetch_related('likes', 'comments__author').order_by('-created_at')
    
    context = {
        'user_profile': profile_user_obj, 
        'posts': posts,
        'form': form
    }
    return render(request, 'profile.html', context)
    

class like_Post(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        liked = False
        if request.user.is_authenticated:
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                liked = False
            else:
                post.likes.add(request.user) 
                liked = True
        
        return JsonResponse({'liked': liked, 'count': post.likes.count()})


class commentPost(View):
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        comment = request.POST.get('comment')
        post.comments.create(content=comment)
        return render(request, 'post_detail.html', {'post': post})
    
class user_update(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.user.pk != pk:
            return HttpResponseForbidden()
        user = get_object_or_404(User, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=user)
        form = UserUpdateForm(initial={
            'username': user.username,
        })
        return render(request, 'user_update.html', {'form': form, 'profile': profile})


    def post(self, request, pk):
        if request.user.pk != pk:
            return HttpResponseForbidden()
        user = get_object_or_404(User, pk=pk)
        profile, _ = Profile.objects.get_or_create(user=user)
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.save()
            if form.cleaned_data.get('profile_picture'):
                profile.profile_picture = form.cleaned_data['profile_picture']
                profile.save()
        return redirect('user_profile', username=user.username)


    
    