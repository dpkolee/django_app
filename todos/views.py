from django.shortcuts import render, redirect
from django.http import HttpResponse
from todos.models import Todo
from django.utils import timezone
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from todos.serializers import TodoSerializer

from .utils import redirect_back




def index(request):
	items=[]
	filter = None

	if request.user.is_authenticated:
		filter = request.GET.get('filter')
		print('Filter=', filter)
		items = filter_results(request.user, filter) 
		
	
	return render(request, 'index.html', {'items': items,'filter':filter})

@login_required
def create(request):

	return render(request, 'create.html', {'form_type': 'create'})

def about(request):

	return render(request, 'about.html')

def contact(request):

	return render(request, 'contact.html')

def login(request):

	return render(request, 'login.html')

def signup(request):

	return render(request, 'signup.html')



def submission(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email = request.POST.get('email')
	first_name = request.POST.get('first_name')
	last_name = request.POST.get('last_name')


	if User.objects.filter(username=username).exists():
		messages.error(request, 'username{} already exists.'.format(username))
		return redirect_back(request)

	if User.objects.filter(email=email).exists():
		messages.error(request, 'email {} already exists.'.format(email))
		return redirect_back(request)

	user= User.objects.create_user(username=username, 
		password=password, 
		email=email, 
		first_name=first_name, 
		last_name=last_name
		)

	messages.info(request, 'user created')

	return redirect('login')



def submit(request):

	username = request.POST.get('username')
	password = request.POST.get('password')

	print('received username and password')
	print('logged in')

	user = auth.authenticate(request,
		username = username,
		password = password
		
		)

	if not user:
		print('login failed')
		messages.error(request, 'Login Failed. Try Again')
		return redirect_back(request)

	auth.login(request, user)
	print('login successful')

	messages.info(request, 'login successful')

	return redirect('index')


def logout(request):
	print('logged out')
	auth.logout(request)
	messages.info(request, 'you have been logged out')
	return redirect('index')

@login_required
def save(request):
	title = request.POST.get('title')
	description = request.POST.get('description')

	form_type = request.POST.get('form_type')
	id = request.POST.get('id')

	print('Form type received:', form_type)
	print('Form todo id received:', id)

	if title is None or title.strip() == '':
		messages.error(request, 'item not saved. Please provide the title.')
		return redirect_back(request)

	if form_type == 'create':
		todo = Todo.objects.create(
		title=title,
		description=description,
		created_at=timezone.now(),
		user= request.user
		)
		messages.info(request,'Todo Item Saved.')

		print('New Todo created: ', todo.__dict__)


	elif form_type == 'edit' and id.isdigit():
		todo = Todo.objects.get(pk = id)

		print('Got todo item: ', todo.__dict__)

		todo.title = title
		todo.description = description
		todo.save()

		print('Todo updated: ', todo.__dict__)

		messages.info(request,'Todo Item Edited.')
	
	return redirect('index')

@login_required
def edit(request, id):

	print('received id = ' +str(id))

	todo = Todo.objects.get(pk = id)

	print('Got todo item: ', todo.__dict__)

	#check if the current ussr is creator user of todo.

	if request.user.id  != todo.user.id:
		messages.error(request, 'YOU ARE NOT AUTHORIZED TO EDIT THIS TODO ITEM.')
		return redirect('index')

	return render(request, 'create.html', {'form_type': 'edit','todo':todo})

@login_required
def remove(request, id):

	todo = Todo.objects.get(pk = id)

	if request.user.id  == todo.user.id:
		todo.delete()
		return redirect('index')


	messages.error(request, 'YOU ARE NOT AUTHORIZED TO REMOVE THIS TODO ITEM.')
	return redirect('index')


def filter_results(user, filter):

	if filter == 'completed':
		return Todo.objects.filter(
			user =user,
			completed =True
			).order_by('-created_at')

	
	elif filter =='pending':
		return Todo.objects.filter(
			user=user, 
			completed = False
			).order_by('-created_at')
	
	else:
		return Todo.objects.filter(user=user).order_by('-created_at')


def hashtags(request):
	title = request.POST.get('title')

	words = title.split('')
	length = len(words)

	for x in range(0,length):
		hashtag = words[x].startswith('#')
		if hashtag == True:
			if len(words[1])==1:
				print('# come with no character attached')

			else:
				hashtags = HashTag.objects.create(title = words[x])

			

class TodoListView(generics.ListCreateAPIView):
	queryset = Todo.objects.all()
	serializer_class = TodoSerializer

class TodoItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
