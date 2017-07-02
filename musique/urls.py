from django.conf.urls import url

from . import views

app_name = 'musique'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^search/$', views.searchTrack, name='search'),
	url(r'^addTrack/$', views.addTrackView, name='addTrackView'),
	url(r'^add/$', views.addTrack, name='add'),
	url(r'^edit/(?P<tid>[0-9]+)/$', views.editTrackView, name='edit'),
	url(r'^edited/$', views.editTrack, name='edited'),
]