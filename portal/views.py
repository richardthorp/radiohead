from datetime import datetime
from time import sleep
from itertools import chain
import json
import stripe
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from profiles.forms import ProfileForm
from checkout.forms import OrderForm
from .models import (PortalTextPost, PortalVideoPost, PortalImagesPost,
                     ImagesPostComment, VideoPostComment, TextPostComment)
from .forms import AddImagesPostForm, AddTextPostForm, AddVideoPostForm

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_public_key = settings.STRIPE_PUBLIC_KEY


# This view ensures that the user is logged in as well as redirecting
# logged in users with active subscriptions
def portal_info(request):
    if str(request.user) != 'AnonymousUser':
        if (request.user.profile.subscription_status == 'active' or
                request.user.is_staff):
            return redirect(reverse('portal_content'))
    return render(request, 'portal/portal_info.html')


# Generate or find Stripe Customer and create a new Subscription
@login_required
def create_portal_customer(request):
    if request.user.is_staff:
        return redirect(reverse('portal_content'))
    email = request.user.email
    user_profile = request.user.profile
    try:
        # If the user profile already has a stripe customer ID, try to
        # retrieve the Stripe customer object associated with the profile
        if user_profile.portal_cust_id:
            try:
                customer = stripe.Customer.retrieve(
                    user_profile.portal_cust_id
                )
                # If the customer object has been deleted on Stripe, create a
                # new stripe customer object
                if 'deleted' in customer.keys():
                    customer = stripe.Customer.create(email=email)

            # Stripe failed to retrieve the customer object
            except Exception:
                customer = stripe.Customer.create(email=email)

        # No customer ID attached to profile - create a new Stripe
        # customer object
        else:
            customer = stripe.Customer.create(email=email)

        # Add the Stripe customer ID to the users profile model
        user_profile.portal_cust_id = customer.id
        user_profile.save()

        # If the user profile has a subscription ID, try to retrieve the
        # subscription from Stripe
        if user_profile.subscription_id:
            try:
                subscription = stripe.Subscription.retrieve(
                    user_profile.subscription_id
                    )
                # If the subscription is active, redirect user to
                # Portal Content
                if subscription.status == 'active':
                    return redirect(reverse('portal_content'))

            # If Stripe returns anything but an active subscription, delete the
            # Subscription ID on the user profile
                else:
                    user_profile.subscription_id = ""
                    user_profile.save()
            except Exception:
                user_profile.subscription_id = ""
                user_profile.save()

        # Create a new subscription for the user
        customer_id = request.user.profile.portal_cust_id
        price_id = settings.SUBSCRIPTION_PRICE_ID

        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{
                'price': price_id,
            }],
            payment_behavior='default_incomplete',
            expand=['latest_invoice.payment_intent'],
            metadata={'email': request.user.email}
        )

        # Save the Subscription ID on the Profile model to use when retrieving
        # subscription
        user_profile.subscription_id = subscription.id
        user_profile.save()
        form = OrderForm(initial={
                        'name': user_profile.default_name,
                        'phone_number': user_profile.default_phone_number,
                        'address_line1': user_profile.default_address_line1,
                        'address_line2': user_profile.default_address_line2,
                        'town_or_city': user_profile.default_town_or_city,
                        'county': user_profile.default_county,
                        'postcode': user_profile.default_postcode,
                        'country': user_profile.default_country,
                    })

        context = {
            'subscription_id': subscription.id,
            'client_secret': (subscription.latest_invoice.
                              payment_intent.client_secret),
            'stripe_public_key': stripe_public_key,
            'portal_price': settings.PORTAL_PRICE,
            'form': form,
        }

        return render(request, 'portal/portal_sign_up.html', context)

    except Exception as e:
        print(e)
        messages.error(request, 'Sorry, there was an issue generating the new subscription, \
            "please try again later')
        return redirect(reverse('portal_info'))


def save_customer_details(request):
    customer_details = {
        'name': request.POST.get('customer_details[name]'),
        'phone_number': request.POST.get('customer_details[phone]'),
        'address_line1': request.POST.get('customer_details[address][line1]'),
        'address_line2': request.POST.get('customer_details[address][line2]'),
        'town_or_city': request.POST.get('customer_details[address][city]'),
        'county': request.POST.get('customer_details[address][state]'),
        'postcode': request.POST.get(
            'customer_details[address][postal_code]'),
        'country': request.POST.get('customer_details[address][country]')
    }

    subscription_id = request.POST['subscription_id']
    stripe.Subscription.modify(
        subscription_id,
        metadata=customer_details,
    )

    if request.POST['save_details'] == 'true':
        profile = request.user.profile
        form = ProfileForm(
            {'default_name': customer_details['name'],
             'default_phone_number': customer_details['phone_number'],
             'default_address_line1': customer_details['address_line1'],
             'default_address_line2': customer_details['address_line2'],
             'default_town_or_city': customer_details['town_or_city'],
             'default_county': customer_details['county'],
             'default_postcode': customer_details['postcode'],
             'default_country': customer_details['country']},
            instance=profile
        )
        if form.is_valid():
            form.save()
    return HttpResponse(status=200)


def update_payment_card(request):
    # Get the customer object
    user_profile = request.user.profile
    customer = stripe.Customer.retrieve(
        user_profile.portal_cust_id
    )
    # Create a new payment intent
    intent = stripe.SetupIntent.create(
        customer=customer['id']
    )
    context = {
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'portal/update_payment_card.html', context)


def set_default_card(request):
    user_profile = request.user.profile
    payment_method_id = request.POST['payment_method_id']
    subscription_id = user_profile.subscription_id

    try:
        stripe.Subscription.modify(
            subscription_id,
            default_payment_method=payment_method_id
        )

        messages.success(request, 'Payment method updated')
        return HttpResponse(status=200)
    except Exception:
        messages.error(request, 'Error updating card details, \
            please try again later.')
        return HttpResponse(status=500)


def cancel_subscription(request, subscription_id):
    try:
        # Cancel the subscription at the end of the current billing period
        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=True
        )
        # Get the subscription end date and format it to render to message
        subscription_end_date = datetime.fromtimestamp(
            subscription.current_period_end
            )
        formatted_end_data = subscription_end_date.strftime("%b %d %Y")
        messages.success(request, f'Subscription Cancelled. \
            You may access the Portal until {formatted_end_data}')
        return redirect(reverse('profile'))
    except Exception as e:
        print(e)


@login_required
def reactivate_subscription(request, subscription_id):
    if request.user.profile.subscription_id == subscription_id:
        stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False
        )
        return redirect(reverse('profile'))
    else:
        messages.error(request, 'You can not reactivate this subscription')
        return redirect(reverse('profile'))


# This view renders the actual portal content for subscribed users
@login_required
def portal_content(request):
    if (request.user.profile.subscription_status == 'active' or
            request.user.is_staff):
        text_posts = PortalTextPost.objects.all()
        video_posts = PortalVideoPost.objects.all()
        images_posts = PortalImagesPost.objects.all()
        all_posts = list(chain(text_posts, video_posts, images_posts))
        context = {
            'posts': all_posts,
            'all': True,
        }
        if request.POST:
            post_filter = request.POST.get('filter')
            if post_filter == 'videos':
                context = {
                    'posts': PortalVideoPost.objects.all(),
                    'videos': True,
                }
            elif post_filter == 'text':
                context = {
                    'posts': PortalTextPost.objects.all(),
                    'text': True,
                }
            elif post_filter == 'images':
                context = {
                    'posts': PortalImagesPost.objects.all(),
                    'images': True,
                }
        return render(request, 'portal/portal_content.html', context)

    else:
        # If the user doesn't have an active subscription status on their
        # profile, allow 5 seconds for the Stripe webhook to be sent to
        # update the profile
        attempt = 1
        active_subscription = False
        while attempt <= 5:
            sleep(1)
            print('ATTEMPT:', attempt)
            profile = Profile.objects.get(user=request.user)
            if profile.subscription_status == 'active':
                active_subscription = True
                break
            attempt += 1
        if active_subscription:
            return render(request, 'portal/portal_content.html')
        else:
            messages.error(request, 'Sorry, you must have an active \
                subscription to Portal to view this page.')
            return redirect(reverse('portal_info'))


# This view renders the portal post detail pages for subscribed users
@login_required
def portal_post_detail(request, post_type, slug):
    if (request.user.profile.subscription_status == 'active' or
            request.user.is_staff):
        if post_type == 'text_post':
            post = PortalTextPost.objects.get(slug=slug)
            template = 'portal/text_post.html'
        if post_type == 'video_post':
            post = PortalVideoPost.objects.get(slug=slug)
            template = 'portal/video_post.html'
        if post_type == 'images_post':
            post = PortalImagesPost.objects.get(slug=slug)
            template = 'portal/images_post.html'

        context = {
            'post': post,
        }

        return render(request, template, context)

    else:
        messages.error(request, 'Sorry, you must have an active \
            subscription to Portal to view this page.')
        return redirect(reverse('portal_info'))


@login_required
def add_portal_post(request, post_type):
    if not request.user.is_staff:
        messages.error(request, 'You must be a staff member add Portal posts.')
        return redirect(reverse('portal_info'))

    if request.method == 'POST':
        if post_type == 'text_post':
            form = AddTextPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save()
                messages.success(request, 'Text post added to Portal')
                return redirect(
                    reverse('portal_post_detail',
                            args=['text_post', post.slug]))
            else:
                messages.error(request, 'Error adding post, please try again.')
                context = {
                    'form': PortalTextPost(request.POST, request.FILES)
                }
                print(form.errors)
                return render(request, 'portal/add_text_post.html', context)

        if post_type == 'video_post':
            form = AddVideoPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save()
                messages.success(request, 'Video post added to Portal')
                return redirect(
                    reverse('portal_post_detail',
                            args=['video_post', post.slug]))
            else:
                messages.error(request, 'Error adding post, please try again.')
                context = {
                    'form': PortalVideoPost(request.POST, request.FILES)
                }
                print(form.errors)
                return render(request, 'portal/add_video_post.html', context)

        if post_type == 'images_post':
            form = AddImagesPostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save()
                messages.success(request, 'Images post added to Portal')
                return redirect(reverse('portal_post_detail',
                                args=['images_post', post.slug]))
            else:
                messages.error(request, 'Error adding post, please try again.')
                context = {
                    'form': PortalImagesPost(request.POST, request.FILES)
                }
                print(form.errors)
                return render(request, 'portal/add_images_post.html', context)

    # GET Request
    if post_type == 'text_post':
        context = {
            'form': AddTextPostForm()
        }
        return render(request, 'portal/add_text_post.html', context)
    if post_type == 'video_post':
        context = {
            'form': AddVideoPostForm()
        }
        return render(request, 'portal/add_video_post.html', context)
    if post_type == 'images_post':
        context = {
            'form': AddImagesPostForm()
        }
        return render(request, 'portal/add_images_post.html', context)


@login_required
def edit_portal_post(request, post_type, post_id):
    if not request.user.is_staff:
        messages.error(request, 'You must be a staff member to edit posts.')
        return redirect(reverse('portal_info'))
    if request.method == 'POST':
        if post_type == 'text_post':
            post = PortalTextPost.objects.get(pk=post_id)
            form = AddTextPostForm(request.POST, request.FILES, instance=post)
        if post_type == 'video_post':
            post = PortalVideoPost.objects.get(pk=post_id)
            form = AddVideoPostForm(request.POST, request.FILES, instance=post)
        if post_type == 'images_post':
            post = PortalImagesPost.objects.get(pk=post_id)
            form = AddImagesPostForm(request.POST, request.FILES,
                                     instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated')
            return redirect(reverse('portal_post_detail',
                                    args=[post_type, post.slug]))
        else:
            print(form.errors)
            messages.error(request,
                           'Error with form data, please check and try again.')
    if post_type == 'text_post':
        post = PortalTextPost.objects.get(pk=post_id)
        form = AddTextPostForm(instance=post)
    if post_type == 'video_post':
        post = PortalVideoPost.objects.get(pk=post_id)
        form = AddVideoPostForm(instance=post)
    if post_type == 'images_post':
        post = PortalImagesPost.objects.get(pk=post_id)
        form = AddImagesPostForm(instance=post)

    context = {
        'form': form,
        'post_type': post_type,
        'post_id': post_id
    }
    return render(request, 'portal/edit_post.html', context)


@login_required
def delete_portal_post(request, post_type, post_id):
    if not request.user.is_staff:
        messages.error(request, 'You must be a staff member to delete posts.')
        return redirect(reverse('portal_info'))
    if post_type == 'text_post':
        post = PortalTextPost.objects.get(pk=post_id)
        post.delete()
    if post_type == 'video_post':
        post = PortalVideoPost.objects.get(pk=post_id)
        post.delete()
    if post_type == 'images_post':
        post = PortalImagesPost.objects.get(pk=post_id)
        post.delete()
    messages.success(request, 'Post Deleted.')
    return redirect(reverse('portal_content'))


# COMMENTS
@login_required
def add_portal_comment(request):
    if not (request.user.profile.subscription_status == 'active' or
            not request.user.is_staff):
        messages.error(request, 'You must have an active subscription \
            to add comments')
        return redirect(reverse('portal_info'))

    posted_by = Profile.objects.get(user=request.POST['user_id'])
    post_id = request.POST['post_id']
    text = request.POST['comment']
    post_type = request.POST['post_type']

    if post_type == 'text_post':
        post = PortalTextPost.objects.get(id=post_id)
        comment = TextPostComment(posted_by=posted_by, text=text,
                                  post=post)
    elif post_type == 'images_post':
        post = PortalImagesPost.objects.get(id=post_id)
        comment = ImagesPostComment(posted_by=posted_by, text=text,
                                    post=post)
    elif post_type == 'video_post':
        post = PortalVideoPost.objects.get(id=post_id)
        comment = VideoPostComment(posted_by=posted_by, text=text,
                                   post=post)
    comment.save()

    return HttpResponse(status=200)


def get_portal_comments(request):
    object_id = request.GET.get('object_id')
    page = request.GET.get('page')
    post_type = request.GET.get('post_type')

    if post_type == 'text_post':
        queryset = TextPostComment.objects.filter(
            post_id=object_id).order_by('-date_posted')
    elif post_type == 'images_post':
        queryset = ImagesPostComment.objects.filter(
            post_id=object_id).order_by('-date_posted')
    elif post_type == 'video_post':
        queryset = VideoPostComment.objects.filter(
            post_id=object_id).order_by('-date_posted')

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


def edit_portal_comment(request):
    post_type = request.POST['post_type']
    comment_id = request.POST['comment_id']
    if post_type == 'text_post':
        comment = TextPostComment.objects.get(pk=comment_id)
    elif post_type == 'images_post':
        comment = ImagesPostComment.objects.get(pk=comment_id)
    elif post_type == 'video_post':
        comment = VideoPostComment.objects.get(pk=comment_id)

    if request.user.profile != comment.posted_by:
        return HttpResponse(status=403)
    else:
        comment.text = request.POST['edited_comment']
        comment.edited = True
        comment.save()
    return HttpResponse(status=200)


def delete_portal_comment(request):
    post_type = request.POST['post_type']
    comment_id = request.POST['comment_id']
    if post_type == 'text_post':
        comment = TextPostComment.objects.get(pk=comment_id)
    elif post_type == 'images_post':
        comment = ImagesPostComment.objects.get(pk=comment_id)
    elif post_type == 'video_post':
        comment = VideoPostComment.objects.get(pk=comment_id)

    if request.user.profile != comment.posted_by and not request.user.is_staff:
        return HttpResponse(status=403)
    else:
        comment.delete()
    return HttpResponse(status=200)
