from django.http import Http404
from django.shortcuts import render
import requests
import json

def index(request):
	try:
		pageNumber = int(request.GET.get('page', 1))
		#check if integer, try with other value: out of range, char
	except Exception:
		raise Http404("Does not exist")

	r = requests.get('http://104.197.128.152:8000/v1/tracks?page=' + str(pageNumber))
	
	hasNext = False
	hasPrev = False
	nextNum = -1
	prevNum = -1
	retVal = []

	jsonRespose = json.loads(r.text)

	if 'next' in jsonRespose and jsonRespose['next']:
		hasNext = True
		nextNum = pageNumber + 1

	if 'previous' in jsonRespose and jsonRespose['previous']:
		hasPrev = True
		prevNum = pageNumber - 1

	if 'results' in jsonRespose:
		retVal = jsonRespose['results']

		for item in retVal:
			item['ratingOld'] = item['rating'] #for edit track
			item['rating'] = int(round(float(item['rating']), 0))

	context = {
		'all_tracks': retVal,
		'isNext': hasNext,
		'isPrev': hasPrev,
		'nextNum': nextNum,
		'prevNum': prevNum
	}
	
	return render(request, 'musique/index.html', context)

def searchTrack(request):
	q = request.GET.get('q')

	parameters = {'title': q}

	r = requests.get('http://104.197.128.152:8000/v1/tracks', params = parameters)
	jsonRespose = json.loads(r.text)
	matchedSongs = []

	#try with different track names (existent and non-existent)

	if 'results' in jsonRespose:
		while jsonRespose['next'] is not None:
			if 'results' in jsonRespose:
				for item in jsonRespose['results']:
					item['ratingOld'] = item['rating'] #for edit track
					item['rating'] = int(round(float(item['rating']), 0))
					matchedSongs.append(item)

			r = requests.get(jsonRespose['next'])
			jsonRespose = json.loads(r.text)

		if 'results' in jsonRespose:
			for item in jsonRespose['results']:
				item['ratingOld'] = item['rating'] #for edit track
				item['rating'] = int(round(float(item['rating']), 0))
				matchedSongs.append(item)

	context = {'matchedTracks': matchedSongs}

	return render(request, 'musique/search.html', context)

def addTrackView(request):
	tid = request.POST.get('id')

	r = requests.get('http://104.197.128.152:8000/v1/genres')

	jsonRespose = json.loads(r.text)
	allGenres = []

	if 'results' in jsonRespose:
		while jsonRespose['next'] is not None:
			if 'results' in jsonRespose:
				for item in jsonRespose['results']:
					allGenres.append(item)

			r = requests.get(jsonRespose['next'])
			jsonRespose = json.loads(r.text)

		if 'results' in jsonRespose:
			for item in jsonRespose['results']:
				allGenres.append(item)

	context = {'allGenres': allGenres}

	return render(request, 'musique/addTrackView.html', context)

def addTrack(request):
	nameVal = request.POST.get('name')
	ratingVal = request.POST.get('rating')
	genreVal = request.POST.getlist('genrelist')

	parameters = {
		'title': nameVal,
		'rating': ratingVal,
		'genres': genreVal
	}

	r = requests.post('http://104.197.128.152:8000/v1/tracks', data = parameters)

	context = {
		'mess': 'Track added.'
	}

	return render(request, 'musique/added.html', context)

def editTrackView(request, tid):
	r = requests.get('http://104.197.128.152:8000/v1/genres')

	jsonRespose = json.loads(r.text)
	allGenres = []

	if 'results' in jsonRespose:
		while jsonRespose['next'] is not None:
			if 'results' in jsonRespose:
				for item in jsonRespose['results']:
					allGenres.append(item)

			r = requests.get(jsonRespose['next'])
			jsonRespose = json.loads(r.text)

		if 'results' in jsonRespose:
			for item in jsonRespose['results']:
				allGenres.append(item)

	r = requests.get('http://104.197.128.152:8000/v1/tracks/' + tid)

	jsonRespose = json.loads(r.text)

	context = {}
		
	context = {
		'trackInfo': jsonRespose,
		'allGenres': allGenres
	}

	return render(request, 'musique/editTrackView.html', context)

def editTrack(request):
	idVal = request.POST.get('id')
	nameVal = request.POST.get('name')
	ratingVal = request.POST.get('rating')
	genreVal = request.POST.getlist('genrelist')

	parameters = {
		'id': idVal,
		'title': nameVal,
		'rating': ratingVal,
		'genres': genreVal
	}

	r = requests.post('http://104.197.128.152:8000/v1/tracks/' + idVal, data = parameters)

	context = {
		'mess': 'Track edited.'
	}

	return render(request, 'musique/added.html', context)