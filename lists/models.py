from django.db import models

class List(models.Model):
	'''жлемент списка'''
	pass

class Item(models.Model):
	'''жлемент списка'''
	text = models.TextField(default = '')
	list = models.ForeignKey(List, on_delete=models.CASCADE, default=None)