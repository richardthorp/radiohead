from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm


@login_required
def profile(request):
    context = {
        'profile': Profile.objects.get(user=request.user),
        'form': ProfileForm(instance=request.user.profile),
    }
    return render(request, 'profiles/profile.html', context)
