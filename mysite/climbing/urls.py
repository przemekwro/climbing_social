from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.loggedin, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('test2/', views.test2, name="test2"),
    path('post/<int:post_id>', views.post_details, name="post_details" )
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)