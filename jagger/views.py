import logging
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.utils import simplejson
from jagger.models import intrest

def home(request):
	return render(request, 'index.html')

def create(request):
	intrests = intrest.objects.all()
	return render(request, 'create.html', {'intrests':intrests})

def entry(request):
	intrests = intrest.objects.all()
	return render(request, 'enter.html', {'intrests':intrests})

def APIInterestGetValues(request):
	rawInput = request.GET.copy()	
	interests = intrest.objects.all()
	ints = {}
	count = 1
	for i in interests:
		datevalpairs = i.dateVals.split(';')
		itemDateVals = {}
		holderItem = {}
		countTwo = 1
		for d in datevalpairs:
			dArray = d.split(':')

			if len(dArray) > 1:
				month = int(dArray[0][4] + dArray [0][5])
				month-=1
				year = dArray[0][:4]
				day = dArray[0][6:]
				holderItem = {'year': year, 'month': month, 'day':day, 'value': dArray[1]}
				itemDateVals[countTwo] = holderItem
				countTwo+=1
		
		singleInterest = {'name': i.name, 'dateVals': itemDateVals}
		ints[count] = singleInterest
		count+=1

	json = simplejson.dumps(ints)
	return HttpResponse(json, mimetype='application/json')
		

def APIInterestCreate(request):
	rawInput = request.GET.copy()	
	interestToMake = intrest(name=rawInput['name'],minVal=rawInput['minVal'],maxVal=rawInput['maxVal'])
	interestToMake.save()
	json = {'code':'200','id':interestToMake.id, 'name':interestToMake.name}
	test = simplejson.dumps(json)
	return HttpResponse(test, mimetype='application/json')		

def APIInterestUpdate(request):
	flag = 200
	rawInput = request.GET.copy()
	d = datetime.now()
	date = d.strftime('%Y%m%d')

	for item in rawInput:
		datapoint = rawInput[item].split(':')
		itemToUpdate = intrest.objects.get(id=datapoint[0])
		dateValues = itemToUpdate.dateVals.split(';')
		for a in dateValues:
			arrayA = a.split(':')

			if arrayA[0] == date:
				flag = 400

		if flag != 400:
			itemToUpdate.dateVals += date + ':' + datapoint[1] + ';'
			itemToUpdate.save()
			json = {'code':'300'}
		else:
			json = {'code':'500'}

	test = simplejson.dumps(json)
	return HttpResponse(test, mimetype='application/json')		

def APIInterestDelete(request):
	rawInput = request.GET.copy()
	cleanId = int(rawInput['id'])
	flag = 200
	try:
		itemToDelete = intrest.objects.get(id = cleanId)

	except:
		flag = 400

	if flag != 400:
		itemToDelete.delete()

	json = {'code':'300','content':{'id':cleanId}}
	test = simplejson.dumps(json)
	return HttpResponse(test, mimetype='application/json')		
