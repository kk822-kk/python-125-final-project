from django import forms
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User





class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'რაზე ფიქრობ?', 
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control d-none',
                'id': 'file-upload'
            })
        }

class RegisterForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'profile_picture']

class UserUpdateForm(forms.Form):
    username = forms.CharField(max_length=150)
    profile_picture = forms.ImageField(required=False)