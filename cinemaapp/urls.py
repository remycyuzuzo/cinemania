from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('login/', views.login_auth),
    path('sign-up/', views.sign_up),
    path('add-new-movie/', views.newMovie, name='newMovie'),
    path('search/', views.searchMovies, name='searchMovies'),
    path('movie-details/<int:movie_id>/', views.movieDetails),
    path('search-actors/', views.searchActors),
    path('logout/', views.logout_auth),
    path('genre/<str:genre>/', views.filter_genre),
    path('delete-movie/<int:movie_id>/', views.deleteMovie),
    path('user/<str:username>/', views.userDetails),
    path('actor/<str:actor_id>/', views.actorDetails)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
