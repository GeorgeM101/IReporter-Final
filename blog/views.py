import folium
from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, HttpResponse, redirect
from .forms import Video_form, SearchForm
from .models import Video, Search
import geocoder


def about(request):
    return render(request, 'blog/about.html', {'title': "About Page"})


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Video upload section


def video(request):
    form = Video_form()
    all_video = Video.objects.all()
    if request.method == "POST":
        form = Video_form(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse("<h1> Uploaded successfully </h1>")
    else:
        form = Video_form()
    return render(request, 'blog/videos.html', {"form": form, "all": all_video})


def map(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('map')
    else:
        form = SearchForm()
    address = Search.objects.all().reverse()
    location = geocoder.osm(address)
    latitude = location.lat
    longitude = location.lng
    country = location.country
    if latitude == None and longitude == None:
        return HttpResponse('Your search is invalid')
    m = folium.Map(location=[19, -12], zoom_start=2)
    folium.Marker([latitude, longitude], tooltip='Click for more',
                  popup=country).add_to(m)
    m = m._repr_html_()

    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'blog/map.html', context)
