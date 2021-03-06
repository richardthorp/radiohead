from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
import requests


def live(request):
    if request.method == 'POST':
        page = request.POST.get('paginate')
    else:
        page = 1
    paginated_data = get_paginated_gigs(page)
    gigs = paginated_data.get('gigs')
    if len(gigs) == 0:
        no_gigs = True
    else:
        no_gigs = False
    return render(request, 'live/live.html',
                  context={'paginated_data': paginated_data,
                           'no_gigs': no_gigs})


def event_detail(request, event_id):
    api_key = settings.SONGKICK_API_KEY
    url = (
        f"https://api.songkick.com/api/3.0/events/"
        f"{event_id}.json?apikey={api_key}"
    )
    response = requests.get(url).json()
    all_details = response['resultsPage']['results']['event']

    # Get string containing all artists performing - add Radiohead to the bill
    # because unfortunately they have no gigs booked!
    artists = 'Radiohead, '
    for artist in all_details['performance']:
        artists += artist['displayName'] + ', '
    # Remove comma and space from last artist name
    artists = artists[:-2]

    event_details = {
        'artists': artists,
        'venue_name': all_details['venue']['displayName'],
        'city': all_details['location']['city'],
        'event_url': all_details['uri'],
        'event_time': all_details['start']['time'],
        'venue_lng': all_details['location']['lng'],
        'venue_lat': all_details['location']['lat'],

    }

    return render(request, 'live/event_detail.html',
                  context={'event_details': event_details})


def get_paginated_gigs(page):
    api_key = settings.SONGKICK_API_KEY
    artist_id = '268425'
    url = (
        f"https://api.songkick.com/api/3.0/artists/"
        f"{artist_id}/calendar.json?apikey={api_key}"
    )
    response = requests.get(url).json()

    gig_list = response['resultsPage']['results']['event']

    paginator = Paginator(gig_list, 10)  # Show 10 gigs per page.
    paginated_gigs = paginator.get_page(page)
    current_page = paginator.page(page)
    has_previous = current_page.has_previous()
    has_next = current_page.has_next()
    next_page = int(page) + 1
    previous_page = int(page) - 1

    gig_details = []
    for gig in paginated_gigs:
        g = {
            'date': gig['start']['date'],
            'event_id': str(gig['id']),
            'city': gig['location']['city'],
            'uri': gig['uri']
        }
        gig_details.append(g)

    paginated_data = {
        'gigs': gig_details,
        'has_previous': has_previous,
        'has_next': has_next,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return paginated_data
