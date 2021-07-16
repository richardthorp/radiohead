from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse
import json
from .models import Single, Comment
from shop.models import Album
from profiles.models import Profile
from .forms import CommentForm


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


def add_comment(request):
    print(request.POST['comment'])
    posted_by = Profile.objects.get(user=request.POST['user_id'])
    on_single = Single.objects.get(id=request.POST['object_id'])
    text = request.POST['comment']
    comment = Comment(posted_by=posted_by, text=text, on_single=on_single)
    comment.save()
    return HttpResponse(status=200)


def get_comments(request):
    object_id = request.GET.get('objectID')
    page = request.GET.get('page')
    queryset = Comment.objects.filter(
        on_single=object_id).order_by('-date_posted')
    paginator = Paginator(queryset, 8)  # Show 8 comments per page.
    paginated_query = paginator.get_page(page)
    current_page = paginator.page(page)
    json_queryset = serializers.serialize('json', paginated_query)

    formatted_data = []
    for comment in json.loads(json_queryset):
        time = comment['fields']['date_posted']
        posted_by = Profile.objects.get(
            pk=int(comment['fields']['posted_by'])
            )
        posted_by_img = posted_by.image.url
        if request.user == posted_by.user:
            comment_permissions = True
        else:
            comment_permissions = False
        data = {
            'time': time,
            'posted_by': posted_by.user.username,
            'id': comment['pk'],
            'posted_by_img': posted_by_img,
            'comment_permissions': comment_permissions,
            'text': comment['fields']['text'],
            'edited': comment['fields']['edited'],
            'has_prev': current_page.has_previous(),
            'has_next': current_page.has_next(),
            'current_page': page,
        }
        formatted_data.append(data)

    return HttpResponse(json.dumps(formatted_data))


def edit_comment(request):
    comment = Comment.objects.get(pk=request.POST['comment_id'])
    if request.user.profile != comment.posted_by:
        return HttpResponse(status=403)
    else:
        comment.text = request.POST['edited_comment']
        comment.edited = True
        comment.save()
    return HttpResponse(status=200)
