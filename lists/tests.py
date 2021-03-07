from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):
	'''тест на токсичность'''

	def test_root_url_resolves_to_home_page_view(self):
		'''тест: корневой url преобразуется в представление домашней страницы'''
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct(self):
		'''тест: домашняя страница возвращает правильный html'''
		response = self.client.get('/')

		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>To-Do list</title>', html)
		self.assertTrue(html.endswith('</html>'))

		self.assertTemplateUsed(response, 'home.html')
