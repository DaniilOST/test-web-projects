from django.contrib import admin
from django.urls import path, include
from main import views as main_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from main.views import UserProfileView, SignUpView, delete_post
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', main_views.test, name="test"),
    path('posts/', main_views.posts, name="posts"),
    path('', main_views.posts, name="main"),  # можно убрать первый аргумент в path
    path('posts/<int:post_id>/', main_views.post, name="post"),
    path('posts/add/free', main_views.add_free, name="add_free"),
    path('posts/add/model', main_views.add_model, name="add_model"),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/profile/', UserProfileView.as_view(), name='user_profile'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

