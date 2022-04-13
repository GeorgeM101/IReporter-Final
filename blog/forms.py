from .models import Video, Search, Post
from django import forms


# class Post(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ('title', 'content', 'image', 'author')


class Video_form(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("caption", "video", "description")


class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ['address', ]
