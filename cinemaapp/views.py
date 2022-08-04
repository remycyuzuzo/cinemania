from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Movie, Actor
from django.core.files.storage import FileSystemStorage

# Create your views here.


def login(request):
    return render(request, 'login.html')


def sign_up(request):
    return render(request, 'sign_up.html')


def index(request):
    movieData = Movie.objects.all()

    return render(request, 'index.html', {'movies': movieData})


def newMovie(request):
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        genre = request.POST.get('genre')
        release_date = request.POST.get('release_date')
        movie_poster = request.FILES.get('poster')
        movie_desc = request.POST.get('synopsis')
        movie_trailer_link = request.POST.get('movie_trailer_link')
        actors = request.POST.get('actors')
        user_id = 1

        fss = FileSystemStorage()
        file = fss.save(movie_poster.name, movie_poster)
        # save all data into the database
        movie = Movie(
            title=movie_title,
            genre=genre,
            release_date=release_date,
            movie_poster=fss.url(file),
            description=movie_desc,
            movie_trailer_link=movie_trailer_link,
            user_id=user_id
        )
        movie.save()

        actors = actors.split(',')
        for actor in actors:
            actor = actor.strip()
            actor_obj = Actor.objects.filter(name=actor)
            if actor_obj:
                movie.actors.add(actor_obj[0])
            else:
                actor_obj = Actor(name=actor)
                actor_obj.save()
                movie.actors.add(actor_obj)

        return HttpResponseRedirect('/')
    else:
        return render(request, 'new-movie.html')


def searchResults(request):
    return render(request, 'search-results.html')


def movieDetails(request):
    return render(request, 'movie-details.html')
