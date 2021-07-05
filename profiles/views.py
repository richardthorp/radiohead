from django.shortcuts import render
from .models import Profile


def profile(request):
    context = {
        'profile': Profile.objects.get(user=request.user)
    }
    return render(request, 'profiles/profile.html', context)