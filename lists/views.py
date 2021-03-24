from django.shortcuts import redirect, render

from lists.models import Item, List

# Create your views here.
def home_page(request):
	'''домашняя страница'''
	return render(request, 'home.html')

def view_list(request):
	'''представление списка'''
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})

def new_list(request):
	'''новый список'''
	list1 = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list1)
	return redirect('/lists/one-of-a-kind-list-in-the-world/')