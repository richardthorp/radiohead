from django.shortcuts import render


# Create your views here.
def media(request):
    return render(request, template_name='media_app/media.html')
