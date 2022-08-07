import email
import json
from webbrowser import get
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render
from .models import CommunityUser, Movie, Actor
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_auth(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to='/')
        else:
            return HttpResponseRedirect(redirect_to='/login')

    return render(request, 'login.html')


def logout_auth(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(redirect_to='/login')
    return HttpResponseRedirect(redirect_to='/')


def sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        image_name = None

        if image:
            fss = FileSystemStorage()
            file = fss.save(image.name, image)
            image_name = fss.url(file)

        user = CommunityUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name
        )
        user.profile_image = image_name
        user.age = age
        user.gender = gender
        user.save()
        return HttpResponseRedirect(redirect_to='/login')
    return render(request, 'sign_up.html')


@login_required(login_url='/login')
def index(request):
    movieData = Movie.objects.all().order_by('-id')
    genres = Movie.objects.values('genre').distinct()
    return render(request, 'index.html', {'movies': movieData, 'genres': genres})


def searchMovies(request):
    if request.method == "GET" and request.GET.get('search'):
        searchKeyword = request.GET.get('search')
        movieResults = Movie.objects.filter(title__icontains=searchKeyword)
        return render(request, 'search-results.html', {'results': movieResults, 'keyword': searchKeyword})
    return HttpResponseRedirect('/')


def filter_genre(request, genre):
    if genre:
        movieData = Movie.objects.filter(genre=genre)
        genres = Movie.objects.values('genre').distinct()
        return render(request, 'index.html', {'movies': movieData, 'filter': genre, 'genres': genres})


@login_required(login_url='/login')
def searchActors(request):
    if request.method == 'GET':
        if request.GET.get('actor') != None and request.GET.get('actor') != '':
            actorName = request.GET.get('actor')
            actorData = Actor.objects.filter(name__icontains=actorName)
            return HttpResponse(json.dumps(list(actorData.values())), content_type="application/json")
        else:
            return HttpResponse(json.dumps([]), content_type="application/json")


@login_required(login_url='/login')
def newMovie(request):
    if request.method == 'POST':
        movie_title = request.POST.get('movie_title')
        genre = request.POST.get('genre')
        release_date = request.POST.get('release_date')
        movie_poster = request.FILES.get('poster')
        movie_desc = request.POST.get('synopsis')
        movie_trailer_link = request.POST.get('movie_trailer_link')
        actors = request.POST.get('actors')
        print(actors)
        user_id = request.user.id
        new_file_name = None
        if movie_poster:
            fss = FileSystemStorage()
            file = fss.save(movie_poster.name, movie_poster)
            new_file_name = fss.url(file)

        # save all data into the database
        movie = Movie(
            title=movie_title,
            genre=genre,
            release_date=release_date,
            movie_poster=new_file_name,
            description=movie_desc,
            movie_trailer_link=movie_trailer_link,
            user_id=user_id
        )
        movie.save()
        actors = actors.split(',')
        if actors:
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


@login_required(login_url='/login')
def movieDetails(request, movie_id):
    movieDetail = Movie.objects.get(id=movie_id)
    if movieDetail:
        return render(request, 'movie-details.html', {'details': movieDetail})
    else:
        return HttpResponseNotFound('404 Not Found')


def deleteMovie(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie and request.user.id == movie.user_id:
        movie.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseNotFound('404 Not Found')


def userDetails(request, username):
    userInfo = CommunityUser.objects.filter(username=username).first()
    if userInfo:
        userMovies = Movie.objects.filter(user__pk=userInfo.id)
        return render(request, 'user-details.html', {'movies': userMovies, 'user_info': userInfo})
    else:
        return HttpResponseNotFound('The user not found')


def actorDetails(request, actor_id):
    actorInfo = Actor.objects.filter(id=actor_id).first()
    if actorInfo:
        actorMovies = Movie.objects.filter(actors__pk=actorInfo.id)
        return render(request, 'actor-details.html', {'movies': actorMovies, 'actorInfo': actorInfo})
    else:
        return HttpResponseNotFound('The user not found')
