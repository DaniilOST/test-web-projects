# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class AddPostFreeForm(forms.Form):
    title = forms.CharField(max_length=200, label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'test_form'}), label="Content")
    post_type = forms.ChoiceField(choices=Post.POST_TYPES, label="Post Type")
    image = forms.ImageField(label="Main image")

    def clean_title(self):
        return self.cleaned_data.get('title', '').strip()

    def clean_post_type(self):
        post_type = self.cleaned_data.get('post_type', '')
        title = self.cleaned_data.get('title', '')
        if post_type == "c" and '(c)' not in title:
            raise ValidationError("The title of a copyright post should contain (c)")
        return post_type

class AddPostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'post_type', 'image')
        labels = {'title': 'Title', 'content': 'Content', 'post_type': 'Post Type', 'image': 'Image'}
        widgets = {'content': forms.Textarea(attrs={'class': 'test_form'})}

    def clean_title(self):
        return self.cleaned_data.get('title', '').strip()

    def clean_post_type(self):
        post_type = self.cleaned_data.get('post_type', '')
        title = self.cleaned_data.get('title', '')
        if post_type == "c" and '(c)' not in title:
            raise ValidationError("The title of a copyright post should contain (c)")
        return post_type

    def clean(self):
        cleaned_data = super().clean()
        # Дополнительные проверки, если необходимо

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']





