from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):
	'''тест на токсичность'''

	def test_uses_home_template(self):
		'''тест: используется домашний шаблон'''
		response = self.client.get('/')

		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		'''тест: можно сохранить пост запрос'''
		response = self.client.post('/', data={'item_text': 'A new list item'})
		self.assertIn('A new list item', response.content.decode())
		self.assertTemplateUsed(response, 'home.html')