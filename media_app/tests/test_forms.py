from django.test import TestCase
from ..forms import CommentForm


class TestCommentForm(TestCase):

    def test_text_field_is_required(self):
        form = CommentForm({'text': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors.keys())

    def test_only_display_text_field(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields, ['text'])