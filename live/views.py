from django.shortcuts import render


def live(request):
    return render(request, 'live/live.html')