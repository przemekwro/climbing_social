from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core import validators

from .models import Post, Comment, UserProfile


class SignUpF(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    content = forms.CharField(widget=forms.Textarea, )

    class Meta:
        model = Post
        fields = ('content','image')


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput, required=False)
    last_name = forms.CharField(widget=forms.TextInput, required=False)
    email = forms.EmailField(widget=forms.TextInput, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        content = forms.CharField(widget=forms.Textarea)
        fields = ('content',)
