from urllib.request import urlopen

from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
import json
from .forms import PostForm, CommentForm, UserChangeForm
from .forms import SignUpF
from .models import Grade, Post, User, Comment, UserProfile, Followers, Like
from django.contrib import messages
# Create your views here.


def get_my_followers(request):
    my_followers = Followers.objects.filter(follow_by=request.user)
    temp = []
    for i in my_followers:
        temp += Post.objects.filter(owner=i.follow_to)
    temp += Post.objects.filter(owner=request.user)
    temp.sort(key=lambda x: x.added_date, reverse=True)
    return temp


def get_my_followers_id(request):
    my_followers = Followers.objects.filter(follow_by=request.user)
    temp = []
    for i in my_followers:
        temp.append(i.follow_to.id)
    temp.append(request.user.id)
    return temp


def get_user_like(request):
    temp = Like.objects.filter(owner=request.user)
    user_like = []
    for i in temp:
        user_like.append(i.post.id)
    return user_like


def register(request):
    if request.method == 'POST':
        form = SignUpF(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = SignUpF()
    form = SignUpF()
    return render(request, 'register.html', {'form': form})


def main(request):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Logged in as: {username}')
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    most_liked = Post.objects.all().order_by('-like_counter')[:3]
    return render(request, 'main.html', {'form': form, 'most_liked':most_liked})


def loggedin(request):
    if request.user.is_authenticated:
        return redirect(request,'')
    return render(request, 'main.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.success(request,"You have to log in to log out. Pleas log in to log out.")
        return redirect('main')
    return redirect('main')


def home(request):
    if request.user.is_authenticated:
        user_like=get_user_like(request)
        post_List = get_my_followers(request)
        paginator = Paginator(post_List,2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        post_List = paginator.get_page(page_number)
        if request.method == 'POST':
            if 'addPost' in request.POST:
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.owner = request.user
                    post.save()
                    messages.success(request,"Post added")
                    return redirect('home')
                else:
                    messages.success(request, "Error occured")
        form = PostForm
        return render(request, 'home.html', {'form': form, 'post_list':post_List, 'page_obj':page_obj, 'user_like':user_like})
    return redirect('main')


def post_details(request,post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid:
                comment = form.save(commit=False)
                comment.owner = request.user
                comment.post = Post.objects.get(id=post_id)
                comment.save()
                messages.success(request,"Comment added")
                post = Post.objects.get(id = comment.post.id)
                post.comment_counter+=1
                post.save()
                #comment_list = Comment.objects.filter(post = post_id).order_by('-added_date')
            else:
                messages.error(request,"Something went wrong")
        post = Post.objects.get(id=post_id)
        try:
            user_like = Like.objects.get(post=post, owner=request.user).post.id
        except Like.DoesNotExist:
            user_like=None
        comment_list = Comment.objects.filter(post=post_id).order_by('-added_date')
        return render(request,'post_details.html',{'post':post, 'comment_list':comment_list,'user_like':user_like})
    return redirect('main')


def friends(request):
    if request.user.is_authenticated:
        friend_list = Followers.objects.filter(follow_by=request.user)
        if request.method == "POST":
            username = request.POST.get('username')
            search_list = User.objects.filter(username__contains=username).exclude(id__in=get_my_followers_id(request))
            if not search_list:
                messages.info(request,"Can't find")
            return render(request,'friends.html',{'friend_list':friend_list,'search_list':search_list,})
        return render(request,'friends.html',{'friend_list':friend_list})
    return redirect('main')


def friends_observe(request,user_id):
    if request.user.is_authenticated:
        if user_id:
            if user_id == request.user.id:
                messages.error(request,'Cannot add myself!')
                return redirect('friends')
            follower = Followers(follow_by=User.objects.get(id=request.user.id),follow_to=User.objects.get(id=user_id))
            follower.save()
            messages.success(request,"Followed new person")

            return redirect('friends')
        else:
            return redirect(request, 'friends')
    else:
        return redirect(request,'main')


def friends_remove(request,follow_id):
    if request.user.is_authenticated:
        if follow_id:
            follow = Followers.objects.get(id=follow_id)
            follow.delete()
            print(follow_id)
            print("usunieto")
            return redirect("friends")
    return redirect('main')


def account_update(request):
    if request.user.is_authenticated:
        post_list = Post.objects.all().filter(owner=request.user)
        form = UserChangeForm
        return render(request,'account_details.html',{'form':form,'post_list':post_list})
    return redirect('main')



def post_like(request):
    print("called by ajax")
    if request.user.is_authenticated:
        if request.method=="POST":
            data = request.POST
            post_id = data['id']
            user_likes = Like.objects.all().filter(owner=request.user)
            post = Post.objects.get(id=post_id)
            for like in user_likes:
                print(like.post.id,post_id,like.owner, request.user)
                if post.id == like.post.id and like.owner == request.user:
                    print("asdads ad ad ad a a")
                    return JsonResponse({'result':'error',})
            like = Like(owner=request.user, post=post)
            post.like_counter += 1
            post.save()
            like.save()
            return JsonResponse({'result':'success', 'post_like':post.like_counter})




