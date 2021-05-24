from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_coffee = User.objects.create_user(username='coffee', password='somepassword')
        self.user_cafe = User.objects.create_user(username='cafe', password='somepassword')

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_art = Category.objects.create(name='art', slug='art')

        self.post_001 = Post.objects.create(
            title='first post',
            content='Hello World',
            category=self.category_programming,
            author=self.user_coffee
        )

        self.post_002 = Post.objects.create(
            title='second post',
            content='Book',
            category=self.category_art,
            author=self.user_cafe,
        )

        self.post_003 = Post.objects.create(
            title='third post',
            content='No content',
            author=self.user_cafe,
        )

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About', navbar.text)

        logo_btn = navbar.find('a', text='Greed')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_btn = navbar.find('a', text='About')
        self.assertEqual(about_btn.attrs['href'], '/about/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_art.name} ({self.category_art.post_set.count()})', categories_card.text)
        self.assertIn(f'Unclassified (1)', categories_card.text)

    def test_post_list(self):
        # If post exists
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('Nothing', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('Unclassified', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)

        self.assertIn(self.user_coffee.username.upper(), main_area.text)
        self.assertIn(self.user_cafe.username.upper(), main_area.text)

        # If post doesn't exists
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('Nothing', main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(
            title='first post',
            content='Hello World',
            author=self.user_coffee,
        )

        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)

        self.assertIn(post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        self.assertIn(self.user_coffee.username.upper(), post_area.text)

        self.assertIn(post_001.content, post_area.text)
