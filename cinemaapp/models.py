from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UserAccountManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("an email address is required for users")
        if not username:
            raise ValueError("username is required")
        if not name:
            raise ValueError("You must provide your name")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            name=name
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CommunityUser(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, verbose_name='email', unique=True)
    profile_image = models.ImageField(
        upload_to='images', blank=True, null=True)
    password = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    # required fields
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True, null=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'password']

    objects = UserAccountManager()

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


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
