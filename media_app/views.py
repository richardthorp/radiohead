import json
from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.core import serializers
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from shop.models import Album
from profiles.models import Profile
from .forms import CommentForm, AddSingleForm
from .models import Single, Comment


def media(request):
    context = {
        'albums': Album.objects.all().order_by('-year')
    }
    return render(request, 'media_app/media.html', context)


def album_singles(request, slug):
    album = Album.objects.get(slug=slug)
    context = {
        'album': album,
        'singles': album.singles.all()
    }
    return render(request, 'media_app/album_singles.html', context)


def single_content(request, album_slug, single_slug):
    single = Single.objects.get(slug=single_slug)
    context = {
        'single': single,
        'comments': Comment.objects.filter(on_single=single.id),
        'form': CommentForm(),
    }
    return render(request, 'media_app/single_content.html', context)


def add_comment(request):
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
        if posted_by.image:
            posted_by_img = posted_by.image.url
        else:
            posted_by_img = (
                f"{settings.MEDIA_URL}profile_pics/default_profile_pic.jpg")
        if request.user == posted_by.user or request.user.is_staff:
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
            'current_page': int(page),
        }
        formatted_data.append(data)

    return JsonResponse(formatted_data, safe=False)


def edit_comment(request):
    comment = Comment.objects.get(pk=request.POST['comment_id'])
    if request.user.profile != comment.posted_by:
        return HttpResponse(status=403)
    else:
        comment.text = request.POST['edited_comment']
        comment.edited = True
        comment.save()
    return HttpResponse(status=200)


def delete_comment(request):
    comment = Comment.objects.get(pk=request.POST['comment_id'])
    if request.user.profile != comment.posted_by and not request.user.is_staff:
        return HttpResponse(status=403)
    else:
        comment.delete()
    return HttpResponse(status=200)


@staff_member_required(login_url='account_login')
def add_single(request):
    if request.method == 'POST':
        form = AddSingleForm(request.POST, request.FILES)
        if form.is_valid():
            single = form.save()
            messages.success(request, f'{str(single)} added to Album')
            return redirect(
                reverse('album_singles', args=[single.album.slug])
                )
        else:
            print(form.errors)
            messages.error(request,
                           'Error adding single, please check form data')
            return render(request, 'media_app/add_single.html', {'form': form})

    form = AddSingleForm()

    return render(request, 'media_app/add_single.html', {'form': form})


@staff_member_required()
def edit_single(request, slug):
    single = Single.objects.get(slug=slug)
    if request.method == 'POST':
        form = AddSingleForm(request.POST, request.FILES, instance=single)
        if form.is_valid():
            single = form.save()
            messages.success(request, f'{str(single)} updated!')
            return redirect(
                reverse('album_singles', args=[single.album.slug])
                )
        else:
            context = {
                'form': form,
                'single': single
            }
            messages.error(request, 'Error with form data, please try again!')
            return render(request, 'media_app/edit_single.html', context)

    form = AddSingleForm(instance=single)
    context = {
        'form': form,
        'single': single
    }

    return render(request, 'media_app/edit_single.html', context)


@staff_member_required()
def delete_single(request, slug):
    single = Single.objects.get(slug=slug)
    album = single.album
    single.delete()
    messages.success(request, 'Single deleted.')

    return redirect(reverse('album_singles', args=[album.slug]))
