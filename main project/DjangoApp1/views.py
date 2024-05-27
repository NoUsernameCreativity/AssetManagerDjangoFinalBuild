from email import message
from getpass import getuser
from msilib.schema import Media
from string import digits
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from Asset_Manager_v_01.settings import INSTALLED_APPS
from .models import teacher, asset, student, User, assetevent
from .forms import AssetEventForm, AssetForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

import json

# debug
from allauth.socialaccount import providers

# for last updated updation
from datetime import datetime

selectedAssetsIndices = []
sortByKey = "id"
filters={'Subject': None}

def index(request):
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'header': "Home page",
            'title' : "Home page",
            'description': "This is the home page"
        }
    )

@login_required(login_url='accounts/login')
def UsersPage(request):
    shownAttributes = ['user_id', 'username', 'Area', 'email']

    # Filter the user attributes from the teacher and student models
    teachers = list(teacher.objects.values())
    students = list(student.objects.values())
    users = []
    for user in teachers+students:
        addDict = user
        if len(addDict) > 0:
            userInfo = User.objects.get(id=addDict['user_id']).__dict__
            # get all info attached to the user
            userInfo = {**addDict, **userInfo}
            # get only fields in shownAttributes and reorder to order shown
            infoOutput = {}
            for key in shownAttributes:
                if key in userInfo.keys():
                   infoOutput[key] = userInfo[key]
            users.append(infoOutput)
    # deal with add assets button to let us do something
    """
    if request.method == 'POST' and 'add_user' in request.POST:
        inputs ={
            'Name': request.POST.get('Name', None),
            'Area': request.POST.get('Area', None)
        }
        if all(inputs.values()): # no 'none' values
            teacher.objects.create(**inputs)
    """

    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'header': "Users page",
            'title' : "Users page",
            'description': "Here you can see all the users of the website.",
            'tableHeaders': ["ID", "Name", "Teaching area", "Email"],
            'tableContent': users,
            'buttons': ['add_user'],
        }
    )

def GetSelectedItemIndex(selectedIndex, dictionary):
    for item in dictionary:
        if item.startswith('selectedassetid'):
            indexOut = int(''.join([char for char in item if char.isdigit()]))
            selectedIndex.append(indexOut)
            return True
    return False

def GetSortByKey(sortByList, dictionary):
    for item in dictionary:
        if item.startswith('sortby'):
            strOut = item.split('_')[1] # must be split around _
            sortByList.append(strOut)
            return True
    return False

@login_required(login_url='accounts/login')
def AssetsPage(request):
    # stuff to deal with forms
    alert = False

    if request.method == 'POST' and 'asset_form' in request.POST:
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            alert = True
        if len(request.FILES.getlist('AssetImage')) > 0:
             storedURL = asset.objects.all().latest('id').__dict__['AssetImage']
             imagefile = request.FILES.getlist('AssetImage')[0]
             print("creating file at" + settings.MEDIA_ROOT.replace('images', '')+storedURL)
             with open(settings.MEDIA_ROOT.replace('images', '')+storedURL, "wb+") as destination:
                for chunk in imagefile.chunks():
                    destination.write(chunk)
    else:
       # check user is a teacher
       form = AssetForm()

    print("checking Alert " + str(alert))

    global filters, sortByKey, selectedAssetsIndices

    # deal with add assets button to let us do something
    selectedAssetIndex = [] # use as mutable type 'out' parameter
    sortByKeytemp = []

    assetList = asset.objects.all().order_by(sortByKey).values()

    if request.method == 'POST':
        if 'add_asset' in request.POST:
            inputs ={
                'Name': request.POST.get('Name', None),
                'Location': request.POST.get('Location', None),
                #'Count': request.POST.get('Value', None),
                'Value': request.POST.get('Value', None),
                'Subject': request.POST.get('Subject', None),
                #'LastUpdated': datetime.now().strftime("%A, %d %B, %Y at %X")
            }
            if all(inputs.values()): # no 'none' values
                asset.objects.create(**inputs)
        elif 'select_all_assets' in request.POST:
            for item in asset.objects.all():
                selectedAssetsIndices.append(item.__dict__['id'])
        elif GetSelectedItemIndex(selectedAssetIndex, request.POST):
            selectedAssetsIndices.append(selectedAssetIndex[0])
        elif GetSortByKey(sortByKeytemp, request.POST):
            sortByKey = sortByKeytemp[0]
        elif 'filter_assets' in request.POST:
            filters = {
                'Subject': request.POST.get('SubjectFilter', None)
            }
            print(filters)
        if filters['Subject'] != None and filters['Subject']!='':
            assetList = asset.objects.filter(**filters).order_by(sortByKey).values()

    selectedAssetString = str(selectedAssetsIndices)
    selectedAssetString = "".join([char for char in selectedAssetString if not char in ['[', ']', ' ']])

    if teacher.objects.filter(user=request.user).exists():
        buttons = ['add_asset', 'select_assets']
    else:
        buttons = ['select_assets']

    # return render
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'page': "Assets",
            'title' : "Assets",
            'content' : "Some Content",
            'tableHeaders': ["ID", "Name", "Location", "Subject", "Value", "Last Updated", "Image"],
            'tableContent': assetList,
            'buttons': buttons,
            'forms': {'assetForm': form},
            'alert': alert,
            'selectedAssets': selectedAssetString
        }
    )

@login_required(login_url='accounts/login')
def SelectedAssetsPage(request):
    global selectedAssetsIndices

    selectedAssetsPost = True

    alert = False
    # create event form
    if request.method == 'POST' and 'create_event' in request.POST:
        form = AssetEventForm(request.POST, request.FILES)
        selectedAssetsPost = False
        if form.is_valid():
            # get comma-separated strings for all the selected assets
            selectedAssetsString = ""
            for index in selectedAssetsIndices:
                selectedAssetsString +=  str(index) + ","
            fields = {
                'LoanExpiry': request.POST.get("LoanExpiry_year", None)+"-"+request.POST.get("LoanExpiry_month", None)+"-"+request.POST.get("LoanExpiry_day", None),
                'UsersInvolved': request.POST.get("UsersInvolved", None),
                'Description': request.POST.get("Description", None),
                'Assets': selectedAssetsString
            }
            # add to database
            assetevent.objects.create(**fields)
            alert = True
    else:
        form = AssetEventForm()

    # edit and deleting selected assets
    if request.method == 'POST':
        if 'edit_selected_assets' in request.POST:
            selectedAssetsPost = False
            inputs ={
                'Name': request.POST.get('Name', None),
                'Location': request.POST.get('Location', None),
                #'Count': request.POST.get('Count', None),
                'Subject': request.POST.get('Subject', None),
                'Value': request.POST.get('Value', None),
            }
            inputs = {k: v for k, v in inputs.items() if v is not None and v is not ''}
            selectedAssetsPost = False
            for index in selectedAssetsIndices:
                asset.objects.filter(pk=index).update(**inputs)
        if 'delete_selected_assets' in request.POST:
            selectedAssetsPost = False
            for index in selectedAssetsIndices:
                asset.objects.get(pk=index).delete()
                selectedAssetsIndices = []
        if 'clear_selected_assets' in request.POST:
            selectedAssetsPost = False

    if request.method == 'POST' and selectedAssetsPost:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        if "UpdatingSelectedAssets" in json_data.values():
            selectedAssetsIndices = []
            for buttonID in json_data['buttonIDs'].split(','):
                digitsString = "".join([char for char in buttonID if char.isdigit()])
                if digitsString != "":
                    selectedAssetsIndices.append(int(digitsString))
            
    print(selectedAssetsIndices)

    assetList = []
    if len(selectedAssetsIndices)>0:
        for index in selectedAssetsIndices:
            dictionary = asset.objects.get(pk=index).__dict__
            del dictionary['_state']
            assetList.append(dictionary)

    # return render
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'page': "Selected Assets",
            'title' : "Selected Assets",
            'content' : "Edit the selected assets here by editing the parameters below and clicking 'edit'",
            'tableHeaders': ["ID", "Name", "Location", "Subject", "Value", "Last Updated", "Image"],
            'tableContent': assetList,
            'form': form,
            'alert': alert,
            'buttons': ['edit_selected_assets', 'add_event'],
        }
    )

def GetAssetNames(foreignKeyString):
    foreignKeyList = [int(char) for char in foreignKeyString.split(',') if char.isnumeric()]
    names = ""
    for index in foreignKeyList:
        if asset.objects.filter(id=index).exists():
            names += asset.objects.get(id=index).__dict__['Name'] + " (Asset " + str(index) + "),"
    return names

def GetUserNames(foreignKeyString):
    foreignKeyList = [int(char) for char in foreignKeyString.split(',') if char.isnumeric()]
    names = ""
    for index in foreignKeyList:
        if User.objects.filter(id=index).exists():
            names += User.objects.get(id=index).__dict__['username'] + " (User " + str(index) + "),"
    return names

@login_required(login_url='accounts/login')
def AssetEventsPage(request): 
    shownAttributes = ['LoanExpiry', 'Assetnames', 'Usernames', 'Description', 'CreationTime']
    events = assetevent.objects.values()

    # code 
    eventsList = []
    for event in events:
        userInfo = event
        if len(event) > 0:
            # Add usernames/asset names as strings
            userInfo['Usernames'] = GetUserNames(event['UsersInvolved'])
            userInfo['Assetnames'] = GetAssetNames(event['Assets'])
            # get only fields in shownAttributes and reorder to order shown
            infoOutput = {}
            for key in shownAttributes:
                if key in userInfo.keys():
                   infoOutput[key] = userInfo[key]
            eventsList.append(infoOutput)

    # return render
    return render(
        request, 
        "DjangoApp1/index.html",  # Relative path from the templates folder to the template file we want
        {
            'page': "Selected Assets",
            'title' : "Selected Assets",
            'content' : "Edit the selected assets here by editing the parameters below and clicking 'edit'",
            'tableHeaders': ["Time", "Assets involved", "Users involved", "Description", "Time Created", ],
            'tableContent': eventsList,
            'buttons': [],
        }
    )

def SignUpPage(request):
    if request.method == 'POST' and 'add_user' in request.POST:
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # log the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # redirect to home page
            print("new account created")
            return HttpResponseRedirect('/home')
    else:
       form = SignUpForm()
    
    # return render
    return render(
        request, 
        "registration/signup.html",  # Relative path from the templates folder to the template file we want
        {
            'form': form
        }
    )