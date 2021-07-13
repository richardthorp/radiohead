from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Album
from .models import Single, Comment
from .forms import CommentForm
from profiles.models import Profile
from django.core import serializers
from django.http import HttpResponse
import json


def media(request):
    context = {
        'albums': Album.objects.all()
    }
    return render(request, 'media_app/media.html', context)


def album_singles(request, album_id):
    context = {
        'album': Album.objects.get(id=album_id),
        'singles': Single.objects.filter(album=album_id)
    }
    return render(request, 'media_app/album_singles.html', context)


def single_content(request, single_id):
    single = Single.objects.get(id=single_id)
    context = {
        'single': single,
        'comments': Comment.objects.filter(on_single=single_id),
        'form': CommentForm(),
    }
    return render(request, 'media_app/single_content.html', context)


def add_comment(request, single_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        single = get_object_or_404(Single, pk=single_id)
        Comment.objects.create(on_single=single,
                               posted_by=request.user.profile,
                               text=form.cleaned_data["text"])
    else:
        print('NOT AL ALL')

    return redirect('single_content', single_id)


def get_comments(reqeust, single_id):
    comments = []
    queryset = Comment.objects.filter(on_single=single_id).order_by('-date_posted')
    json_queryset = serializers.serialize('json', queryset)
    for comment in json.loads(json_queryset):
        time = comment['fields']['date_posted']
        posted_by = Profile.objects.get(
            pk=int(comment['fields']['posted_by'])
            )
        posted_by_img = posted_by.image.url
        comments.append({
            'time': time,
            'posted_by': posted_by.user.username,
            'posted_by_img': posted_by_img,
            'text': comment['fields']['text']
        })
    print(comments)
    return HttpResponse(json.dumps(comments), content_type='application/json')
