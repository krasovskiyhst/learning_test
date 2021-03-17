from django.db import models

class Item(models.Model):
	'''жлемент списка'''
	text = models.TextField(default = '')
