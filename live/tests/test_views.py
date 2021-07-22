from django.test import TestCase
from django.shortcuts import reverse


class TestLiveViews(TestCase):

    def test_live_view(self):
        url = reverse('live', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('paginated_data', response.context.keys())
        self.assertTemplateUsed(response, 'live/live.html')

    def test_event_detail_view(self):
        # Get an event_id from the Songkick API to use in the test
        api_url = reverse('live', args=[1])
        api_response = self.client.get(api_url)
        event_id = (
            api_response.context['paginated_data']['gigs'][0]['event_id']
            )

        url = reverse('event_detail', args=[event_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('event_details', response.context.keys())
        self.assertTemplateUsed(response, 'live/event_detail.html')
