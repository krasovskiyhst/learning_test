from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase):
	'''тест на токсичность'''

	def test_uses_home_template(self):
		'''тест: используется домашний шаблон'''
		response = self.client.get('/')

		self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):
	'''тест модели жлемента списка'''

	def test_saving_and_retrieving_items(self):
		'''тест сохранения и получения элементов списка'''
		list1 = List()
		list1.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list1
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list1
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, list1)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list1)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list1)

class ListViewTest(TestCase):
	'''тест представления списка'''

	def test_uses_list_template(self):
		'''тест: используется шаблон списка'''
		list1 = List.objects.create()
		response = self.client.get(f'/lists/{list1.id}/')
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		'''тест: отображаются элементы только для этого списка'''
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='другой элемент 1 списка', list=other_list)
		Item.objects.create(text='другой элемент 2 списка', list=other_list)

		response = self.client.get(f'/lists/{correct_list.id}/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'другой элемент 1 списка')
		self.assertNotContains(response, 'другой элемент 2 списка')

	def test_passes_correct_list_to_template(self):
		'''Тест: передаётся правильный шаблон списка'''
		other_list = List.objects.create()
		correct_list =  List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)

class NewListTest(TestCase):
	'''тест нового списка'''
	def test_can_save_a_POST_request(self):
		'''тест: можно сохранить post-запрос'''
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		'''тест: переадресует после post-запроса'''
		response = self.client.post('/lists/new', data={'item_text': 'A newlist item'})
		new_list = List.objects.first()
		self.assertRedirects(response, f'/lists/{new_list.id}/')

class NewItemTest(TestCase):
	'''тест нового элемента списка'''
	def test_can_save_a_POST_request_to_an_existing_list(self):
		'''тест: можно сохранить post-запрос в существующий список'''
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		'''тест: переадресуется в представление списка'''
		other_list = List.objects.create()

		correct_list = List.objects.create()
		response = self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')