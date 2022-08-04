from django import forms


class MovieForm(forms.Form):
    title = forms.CharField(max_length=255)
    genre = forms.Select(choices=[('Action', 'Action'), ('Comedy', 'Comedy'), (
        'Drama', 'Drama'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Sci-Fi', 'Sci-Fi')])
    release_date = forms.DateField()
    actors = forms.CharField()
    description = forms.Textarea()
    movie_poster_image = forms.ImageField(required=False, label='Movie Poster Image',
                                          help_text='Upload a movie poster image', widget=forms.FileInput(attrs={'class': 'form-control'}))
    movie_trailer_link = forms.CharField()
