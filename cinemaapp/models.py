from django.db import models

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CommunityUser(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    profile_image = models.ImageField(
        upload_to='profile_images', blank=True, null=True)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    # year = models.IntegerField()
    actors = models.ManyToManyField(Actor)
    movie_poster = models.ImageField(
        null=True, blank=True, upload_to='images/')
    release_date = models.DateField(null=True)
    movie_trailer_link = models.TextField(null=True)
    date_time_added = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=CommunityUser, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.title
