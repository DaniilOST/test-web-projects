# views.py
from django.contrib import messages
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Author
from .forms import AddPostFreeForm, AddPostModelForm, SignUpForm
from django.http import HttpResponseServerError
from django.http import Http404
from django.core.exceptions import ValidationError


def test(request):
    now = datetime.now()
    print(now)
    return render(request, 'test.html', {'time': now})

def posts(request):
    posts = Post.objects.all()
    return render(request, 'posts.html', {'posts': posts})

def post(request, post_id):
    try:
        p = Post.objects.get(id=post_id)
        return render(request, 'post.html', {'p': p})
    except Post.DoesNotExist:
        raise Http404("Пост не найден")

def add_free(request):
    try:
        if request.method == 'POST':
            form = AddPostFreeForm(request.POST, request.FILES)
            if form.is_valid():
                post_entry = form.save(commit=False)
                post_entry.author = request.user.author if request.user.is_authenticated else None
                post_entry.save()
                return redirect('post', post_entry.id)
        else:
            form = AddPostFreeForm()
        return render(request, 'add_free_form.html', {'form': form})
    except ValidationError as e:
        messages.error(request, f"Ошибка валидации: {e}")
        return render(request, 'add_free_form.html', {'form': form})

def add_model(request):
    if request.method == 'POST':
        form = AddPostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post_entry = form.save(commit=False)
            
            if request.user.is_authenticated:
                # Если пользователь аутентифицирован, убедимся, что у него есть связанный объект Author
                author, created = Author.objects.get_or_create(user=request.user, defaults={'name': request.user.username, 'email': request.user.email})
                post_entry.author = author
            
            post_entry.save()
            return redirect('post', post_entry.id)
    else:
        form = AddPostModelForm()
    
    return render(request, 'add_free_form.html', {'form': form})


@login_required
def add_free(request):
    if request.method == 'POST':
        form = AddPostFreeForm(request.POST, request.FILES)
        if form.is_valid():
            post_entry = form.save(commit=False)
            post_entry.author = request.user.author if request.user.is_authenticated else None
            post_entry.save()
            return redirect('post', post_entry.id)
    else:
        form = AddPostFreeForm()
    return render(request, 'add_free_form.html', {'form': form})

@login_required
def add_model(request):
    if request.method == 'POST':
        form = AddPostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post_entry = form.save(commit=False)
            
            if request.user.is_authenticated:
                # Если пользователь аутентифицирован, убедимся, что у него есть связанный объект Author
                author, created = Author.objects.get_or_create(user=request.user, defaults={'name': request.user.username, 'email': request.user.email})
                post_entry.author = author
            
            post_entry.save()
            return redirect('post', post_entry.id)
    else:
        form = AddPostModelForm()
    
    return render(request, 'add_free_form.html', {'form': form})

class UserProfileView(LoginRequiredMixin, View):
    template_name = 'registration/user_profile.html'

    def get(self, request, *args, **kwargs):
        # Добавьте вашу логику для отображения профиля пользователя
        return render(request, self.template_name)

class SignUpView(View):
    template_name = 'main/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile')  # Замените на имя вашего представления профиля пользователя
        return render(request, self.template_name, {'form': form})
    
@login_required
def delete_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)

        # Проверьте, является ли текущий пользователь автором поста
        if post.author.user != request.user:
            messages.error(request, "Вы не можете удалить этот пост.")
            return redirect('post', post_id=post_id)

        if request.method == 'POST':
            post.delete()
            messages.success(request, "Пост успешно удален.")
            return redirect('posts')
        else:
            return render(request, 'confirm_delete_post.html', {'post': post})
    except Exception as e:
        # Обработка любых других исключений, например, если что-то пошло не так
        messages.error(request, f"Ошибка: {e}")
        return HttpResponseServerError("<h3>Internal Server Error</h3>")
