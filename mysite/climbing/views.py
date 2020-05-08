from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import PostForm, CommentForm
from .forms import SignUpForm
from .models import Grade, Post, User, Comment
from django.contrib import messages
# Create your views here.


class postList(ListView):
    paginate_by = 2
    model = Post

def test(request):
    print("wyswietlono strone")
    message = "message";
    messages.success(request, f"New account created: {message}")
    return render(request, 'test2.html')

def test2(request):
    print("wyswietlono strone")
    return render(request, 'test2.html')



def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = SignUpForm()
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
    most_liked = Post.objects.all().order_by('-comment_counter')[:3]
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
        if request.method == 'POST':
            if 'addPost' in request.POST:
                form = PostForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.owner = request.user
                    post.save()
                    messages.success(request,"Post added")
                    form = PostForm
                    post_List= Post.objects.all().order_by('-added_date')

                    paginator = Paginator(post_List, 12)  # Show 25 contacts per page.
                    page_number = request.GET.get('page')
                    page_obj = paginator.get_page(page_number)
                    post_List = paginator.get_page(page_number)
                    return render(request, 'home.html', {'form': form, 'postList': post_List, 'page_obj': page_obj,})
                else:
                    messages.success(request, "Error occured")
                print("odebrano formularz post");
            elif 'addRoute' in request.POST:
                print("odebrano formularz route")
        form = PostForm
        post_List = Post.objects.all().order_by('-added_date')

        paginator = Paginator(post_List, 12)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        post_List = paginator.get_page(page_number)
        return render(request, 'home.html', {'form': form, 'postList':post_List, 'page_obj':page_obj})
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
                return redirect('post_details', post_id=post_id)
            else:
                messages.error(request,"Something went wrong")
                return redirect(request,"post_details")

        post = Post.objects.get(id=post_id)
        comment_list = Comment.objects.filter(post=post_id).order_by('-added_date')
        return render(request,'post_details.html',{'post':post, 'comment_list':comment_list})
    return redirect('main')
