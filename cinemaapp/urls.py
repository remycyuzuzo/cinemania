from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('sign-up/', views.sign_up),
    path('add-new-movie/', views.newMovie, name='newMovie'),
    path('search/', views.searchResults),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
