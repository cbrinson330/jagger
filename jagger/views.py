import logging
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render
from django.utils import simplejson
from jagger.models import intrest
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Display Pages
def loginPage(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/track')
	else:
		return render(request, 'login.html')

def logoutUser(request):
		logout(request)
		return HttpResponseRedirect('/')

def home(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return render(request, 'index.html')

def create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		intrests = intrest.objects.filter(owner = request.user)
		return render(request, 'create.html', {'intrests':intrests})

def entry(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		intrests = intrest.objects.filter(owner = request.user)
		return render(request, 'enter.html', {'intrests':intrests})

# Helper Functions 

def loginUser(httpRequest, userInfo, password):
	data = {'code':'200','error':'none'}
	userA = authenticate(username=userInfo, password=password)
	if userA is not None:
		if userA.is_active:
			logging.warning('line46')
			login(httpRequest, userA)
			data = {'code':'200','eror':'none'}
		else:
			data = {'code':'500','error':'Your account has been disabled'}
	else:
		data = {'code':'500','error':'Invalid login'}
	
	return data
		

# API Functions

def APIInterestLogin(request):
	rawInput = request.GET.copy()
	inputUsername = rawInput['username']
	inputPassword = rawInput['password']
	data = {'code':'200','error':'none'}
	
	userB = authenticate(username=inputUsername, password=inputPassword)
	if userB is not None:
		if userB.is_active:
			userResponse = loginUser(request, userB, inputPassword)
		else:
			data = {'code':'500','error':'account has been disabled'}
	else:
		data = {'code':'500','error':'Invalid CREDS...GOTTA GET THOSE CREDS MAN'}

	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
	

def APIInterestRegister(request):
	rawInput = request.GET.copy()
	username = rawInput['username']
	password = rawInput['password']
	email = rawInput['email']
	userHolder = None 
	data = None

	try:
		userHolder = User.objects.create_user(username,email,password)
	except:
		data = {'code':'500','error':'Username already taken'}

	if userHolder is not None:
		loginUserResponse = loginUser(request, userHolder, password)
		if loginUserResponse['code'] != '500':
			data = {'code':'200','error':'none'}
		else:
			data = {'code':'500','error':'There was an issue with logging you in'}
	else:
		if data is None:
			data = {'code':'500','error':'There was an issue creating your user'}

	json = simplejson.dumps(data)
	return HttpResponse(json, mimetype='application/json')
	

def APIInterestGetValues(request):
	rawInput = request.GET.copy()	
	interests = intrest.objects.filter(owner = request.user)
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
	interestToMake = intrest(name=rawInput['name'],minVal=rawInput['minVal'],maxVal=rawInput['maxVal'],owner=request.user)
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

		if flag != 400 and itemToUpdate.owner == request.user:
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

	if flag != 400 and request.user == itemToDelete.owner:
		itemToDelete.delete()
		json = {'code':'300','content':{'id':cleanId}}

	else:
		json = {'code':'500','content':'permissions error'}

	test = simplejson.dumps(json)
	return HttpResponse(test, mimetype='application/json')		
