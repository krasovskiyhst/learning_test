from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest

# Create your tests here.

class HomePageTest(TestCase):
	'''тест на токсичность'''

	def test_home_page_returns_correct_html(self):
		'''тест: используется домашний шаблон'''
		response = self.client.get('/')

		self.assertTemplateUsed(response, 'home.html')
