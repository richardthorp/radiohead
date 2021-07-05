from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import Profile
from .forms import ProfileForm


@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        else:
            print('Form not valid')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'profile': profile,
        'form': form,
    }

    return render(request, 'profiles/profile.html', context)
