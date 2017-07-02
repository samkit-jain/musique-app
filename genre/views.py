from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
import requests
import json

@ensure_csrf_cookie
def genres(request, pageNumber):
	r = requests.get('http://104.197.128.152:8000/v1/genres?page=' + pageNumber)
	
	hasNext = False
	hasPrev = False
	nextNum = -1
	prevNum = -1
	retVal = []

	jsonRespose = json.loads(r.text)

	if 'next' in jsonRespose and jsonRespose['next']:
		hasNext = True
		nextNum = int(pageNumber) + 1

	if 'previous' in jsonRespose and jsonRespose['previous']:
		hasPrev = True
		prevNum = int(pageNumber) - 1

	if 'results' in jsonRespose:
		retVal = jsonRespose['results']

	context = {
		'all_genres': retVal,
		'isNext': hasNext,
		'isPrev': hasPrev,
		'nextNum': nextNum,
		'prevNum': prevNum
	}
	
	return render(request, 'genre/genres.html', context)

def addGenre(request):
	#error handling
	parameters = {
		'name': request.POST.get('name')
	}

	r = requests.post('http://104.197.128.152:8000/v1/genres', data = parameters)

	context = {
		'mess': 'Genre added.'
	}

	return render(request, 'genre/editgenres.html', context)

def editGenre(request):
	mess = "Genre edited."

	if request.POST.get('name') == "":
		mess = "Genre not edited. Empty string."
	else:
		parameters = {
			'id': int(request.POST.get('id')),
			'name': request.POST.get('name')
		}

		r = requests.post('http://104.197.128.152:8000/v1/genres/' + request.POST.get('id'), data = parameters)

	context = {
		'mess': mess,
	}

	return render(request, 'genre/editgenres.html', context)