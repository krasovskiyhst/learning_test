from django.shortcuts import redirect, render

from lists.models import Item, List

# Create your views here.
def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')

def view_list(request, list_id):
	'''представление списка'''
	list1 = List.objects.get(id=list_id)
	return render(request, 'list.html', {'list': list1})

def new_list(request):
	'''новый список'''
	list1 = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list1)
	return redirect(f'/lists/{list1.id}/')

def add_item(request, list_id):
	'''добавить элемент'''
	list1 = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list1)
	return redirect(f'/lists/{list1.id}/')