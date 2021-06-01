from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from blog.models import Post

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_cafe = User.objects.create_user(username='cafe', password='somepassword')

    def test_landing(self):
        post_001 = Post.objects.create(
            title='first post',
            content='Hello World',
            author=self.user_cafe
        )

        post_002 = Post.objects.create(
            title='second post',
            content='Book',
            author=self.user_cafe
        )

        post_003 = Post.objects.create(
            title='third post',
            content='No content',
            author=self.user_cafe
        )

        post_004 = Post.objects.create(
            title='fourth post',
            content='444444444',
            author=self.user_cafe
        )

        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        body = soup.body
        self.assertNotIn(post_001.title, body.text)
        self.assertIn(post_002.title, body.text)
        self.assertIn(post_003.title, body.text)
        self.assertIn(post_004.title, body.text)
