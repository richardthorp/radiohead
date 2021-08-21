from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, template_name="home/index.html")


@login_required
def admin_hub(request):
    if not request.user.is_staff:
        return redirect(reverse('home'))
    else:
        return render(request, 'home/admin-hub.html')
