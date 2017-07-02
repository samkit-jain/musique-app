from django.conf.urls import url

from . import views

app_name = 'genre'
urlpatterns = [
	url(r'^(?P<pageNumber>[1-9][0-9]*)/$', views.genres, name='genres'),
	url(r'^addGenre/$', views.addGenre, name='addgenres'),
	url(r'^editGenre/$', views.editGenre, name='editgenres'),
]