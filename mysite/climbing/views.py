from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
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

def grades(request):
    grades = Grade.objects.all()
    return render(request, 'test.html',)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'test.html', {'form': form})

