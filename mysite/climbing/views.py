from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import SignUpForm
from .models import Grade
from django.contrib import messages
# Create your views here.



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
    if request.method == "POST":
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
    return render(request, 'main.html', {'form': form})

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
        return render(request, 'home.html',)
    return redirect('main')
