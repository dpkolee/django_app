from django.conf.urls import url
from todos import views

urlpatterns =  [
	url(r'^$',views.index, name='index'),
	url(r'^create$',views.create, name='create'),
	url(r'^about$',views.about, name='about'),
	url(r'^contact$',views.contact, name='contact'),
	url(r'^save$',views.save, name='save'),
	url(r'^edit/todos/(\d+)$',views.edit, name='edit'),
	url(r'^remove/todos/(\d+)$',views.remove, name='remove'),
	url(r'^login$',views.login, name='login'),
	url(r'^submit$',views.submit, name='submit'),
	url(r'^logout$',views.logout, name='logout'),
	url(r'^signup$',views.signup, name='signup'),
	url(r'^submission$',views.submission, name='submission'),
	url(r'^api/todos$',views.TodoListView.as_view(), name='api_todo_list'),
	url(r'^api/todos/(?P<pk>[0-9]+)$', views.TodoItemView.as_view(), name='api_todo_item'),


]