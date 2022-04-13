from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account Successfully Created for {username} Login In Now!!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def profile_update(request):
    form = ProfileUpdateForm()
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image')
        profile = Profile.objects.filter(user = user)
        if profile.exists():
            profile = Profile.objects.get(user = user)
            profile.image = image
            profile.save()

            return redirect('/profile/')

        else:
            new_profile = Profile(user = user, image=image)
            new_profile.save()

            return redirect('/profile/')
            
    context = {
        'form': form
    }

    return render(request, 'users/profile_update.html', context)
