from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):
	'''тест нового посетителя'''

	def setUp(self):
		'''установка'''
		self.browser = webdriver.Firefox()

	def tearDown(self):
		'''демонтаж'''
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		'''Подтверждение строки в таблице списка'''
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrive_it_later(self):
		'''можно начать список и получить его позже'''

		# Клиент решил посетить приложение со списком неотложных дел
		self.browser.get('http://localhost:8000')

		# Клиент видит, что заголовок и шапка стр говорят о списках дел
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# Клиенту предлагается ввести элемент списка
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# Клиент набирает в текстовом поле "Кпить павлиньи перья"
		inputbox.send_keys('Купить павлиньи перья')


		# Когда клиент нажимает enter, станица обновляется, и теперь
		# страница содержит "1: Купить павлиньи перья" в качестве элемента списка
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		self.check_for_row_in_list_table('1: Купить павлиньи перья')


		# Текстовое поле по-прежнему приглашает ее добавить еще один элемент.
		# Она вводит "Сделать мушку из павлиньих перьев" 
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Сделать мушку из павлиньих перьев')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)
		


		# Страница снова обновляется, и теперь показывает оба элемента ее списка
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.check_for_row_in_list_table('1: Купить павлиньи перья')
		self.check_for_row_in_list_table('2: Сделать мушку из павлиньих перьев')

		# Эдит интересно, запомнит ли сайт ее список. Далее она видит, что
		# сайт сгенерировал для нее уникальный URL-адрес – об этом
		# выводится небольшой текст с объяснениями.
		self.fail('Закончить тест')

		# Она посещает этот URL-адрес – ее список по-прежнему там.
		# Удовлетворенная, она снова ложится спать

if __name__ == '__main__':
	unittest.main(warnings='ignore')