from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name="signup"),
    path('test2/', views.test2, name="test2"),
    path('grades/', views.grades, name="grades"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)