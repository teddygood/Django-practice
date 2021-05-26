from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_coffee = User.objects.create_user(username='coffee', password='somepassword')
        self.user_cafe = User.objects.create_user(username='cafe', password='somepassword')

        self.user_cafe.is_staff = True
        self.user_cafe.save()

        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_art = Category.objects.create(name='art', slug='art')

        self.tag_python = Tag.objects.create(name='python', slug='python')
        self.tag_javascript = Tag.objects.create(name='javascript study', slug='javascript-study')
        self.tag_java = Tag.objects.create(name='java study', slug='java-study')

        self.post_001 = Post.objects.create(
            title='first post',
            content='Hello World',
            category=self.category_programming,
            author=self.user_coffee
        )
        self.post_001.tags.add(self.tag_java)

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
        self.post_003.tags.add(self.tag_python)
        self.post_003.tags.add(self.tag_javascript)

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
        self.assertIn(f'{self.category_programming.name} ({self.category_programming.post_set.count()})',
                      categories_card.text)
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
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertIn(self.tag_java.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_javascript.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertNotIn(self.tag_java.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_javascript.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('Unclassified', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)
        self.assertNotIn(self.tag_java.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_javascript.name, post_003_card.text)

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
        # post_001 = Post.objects.create(
        #     title='first post',
        #     content='Hello World',
        #     author=self.user_coffee,
        # )

        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.tag_java.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_javascript.name, post_area.text)

        self.assertIn(self.user_coffee.username.upper(), post_area.text)

        self.assertIn(self.post_001.content, post_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.category_programming.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_java.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_java.name, soup.h1.text)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_java.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post(self):
        # If not logged in status code != 200
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # not staff login
        self.client.login(username='coffee', password='somepassword')

        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        # staff login
        self.client.login(username='cafe', password='somepassword')

        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Create a Post Form',
                'content': "Let's create a Post Form page",
                'tags_str': 'new tag; 한글, python'
            }
        )
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Create a Post Form")
        self.assertEqual(last_post.author.username, 'cafe')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글'))
        self.assertEqual(Tag.objects.count(), 5)

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'

        # if not logged in
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # if logged in, but not author
        self.assertNotEqual(self.post_003.author, self.user_coffee)
        self.client.login(
            username=self.user_coffee.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)

        # if author
        self.client.login(
            username=self.user_cafe.username,
            password='somepassword'
        )
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('python; javascript study', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title': 'Revise the third post.',
                'content': 'Gray',
                'category': self.category_programming.pk,
                'tags_str': 'python; 한글, some tag'
            },
            follow=True
        )

        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')

        self.assertIn('Revise the third post.', main_area.text)
        self.assertIn('Gray', main_area.text)
        self.assertIn(self.category_programming.name, main_area.text)

        self.assertIn('python', main_area.text)
        self.assertIn('한글', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('javascript study', main_area.text)