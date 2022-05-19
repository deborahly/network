from django.test import TestCase
from .models import User, Post


# Create your tests here.

class NewTestCase(TestCase):

    def setUp(self):
        # Create user
        user = User.objects.create_user(username="Gigi", email="gigi@example.com", password="12345")

        # Create posts
        good_post = Post.objects.create(poster=user, content="My name is Bridgette, but you can call me Gigi.")
        empty_post = Post.objects.create(poster=user, content="")
        too_long_post = Post.objects.create(poster=user, content="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

    def test_good_post(self):
        user = User.objects.get(username="Gigi")
        p = Post.objects.get(content="My name is Bridgette, but you can call me Gigi.")
        self.assertEqual(p.poster, user)

    def test_empty_post(self):
        user = User.objects.get(username="Gigi")
        p = Post.objects.get(content="")
        self.assertFalse(p.is_valid_post())

    def test_too_long_post(self):
        user = User.objects.get(username="Gigi")
        p = Post.objects.get(content="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        self.assertFalse(p.is_valid_post())
        
