from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('account/details/<int:account_id>', views.account_details, name="account_details"),
    path('login/', views.loggedin, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('post/<int:post_id>', views.post_details, name="post_details" ),
    path('friends/', views.friends, name="friends"),
    path('friends/observe/<int:user_id>', views.friends_observe,),
    path('friends/delete/<int:follow_id>', views.friends_remove, ),
    url('post/like/', views.post_like, name="post_like"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)