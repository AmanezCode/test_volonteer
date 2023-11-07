from django.shortcuts import render
from .models import Profile, Organization, Volunteer, Event
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404

def setting(request, userType):
    return render(request, 'settings.html', {'user_type': userType,'username': request.user})

def updateOrgSetting(request):
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(Profile, userName=user)

        orgName = request.POST.get('orgName')
        orgDivision = request.POST.get('orgDivision')
        
        try:
            organization = Organization.objects.get(profile=profile)
            organization.profile = profile
            organization.orgName = orgName
            organization.orgDivision = orgDivision
            organization.save()
        except:
            organization = Organization(profile=profile, orgName=orgName, orgDivision=orgDivision)
            organization.save()

        userName = request.user.username

        return redirect("/loadHomepage/" + userName + "/")
    else:
        return render(request, 'registrationapp/login.html')

def update_profile(request):
    if request.method == 'POST':
        user = request.user
        profile = get_object_or_404(Profile, userName=user)
        skills = request.POST.get('skills')
        highLevelEducation = request.POST.get('education')
        try:
            volunteer = Volunteer.objects.get(profile=profile)
            volunteer.profile = profile
            volunteer.skills = skills
            volunteer.highLevelEducation = highLevelEducation
            volunteer.save()
        except:
            volunteer = Volunteer(profile=profile, skills=skills, highLevelEducation=highLevelEducation)
            volunteer.save()
        message = "Your skills have been saved"
        allEvents = Event.objects.all()

        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'username': user, 'events': allEvents})

def event_creation(request,username):
    if request.method == 'POST':
        eventName = request.POST['event_name']
        profile = get_object_or_404(Profile, userName=request.user)
        organization = get_object_or_404(Organization, profile=profile)
        event_description = request.POST['event_description']
        event_type = request.POST['event_type']
        no_of_positions = int(request.POST['no_of_positions'])
        location = request.POST['location']
        date = request.POST['date']
        stime = request.POST['stime']
        etime = request.POST['etime']
        
        event = Event.objects.create(eventName=eventName, organization=organization, eventDescription=event_description, eventType=event_type, noOfPositions=no_of_positions, location=location, eventDate=date, startTime=stime, endTime=etime)
        
        event.save()

        userName = request.user.username

        return redirect("/loadHomepage/" + userName + "/")
    else:
        return render(request, 'event_creation.html', {'message': 'hi', 'user_type': 2, 'username': request.user})

def deleteEvent(request, eventId, username):
    event = Event.objects.get(id=eventId)
    event.delete()
    profile = Profile.objects.get(userName = username)
    allEvents = []
    message = ""
    if profile.userType==1:
        return render(request, 'homepage.html', {'message': message, 'user_type': 1})
    else:
        try:
            organization = Organization.objects.get(profile=profile)
            allEvents = Event.objects.filter(organization = organization)
        except:
            organization = ""
        return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})
    
def loadHomepage(request, username):
    profile = Profile.objects.get(userName = username)
    allEvents = []
    message = ""
    if profile.userType==1:
        allEvents = Event.objects.all()
        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'username': username, 'events': allEvents})
    else:
        try:
            organization = Organization.objects.get(profile=profile)
            allEvents = Event.objects.filter(organization = organization)
        except:
            organization = ""
        return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})

def registerEvent(request, eventId, username):
    profile = Profile.objects.get(userName = username)
    if not Volunteer.objects.filter(profile=profile).exists():
        message = "Please update Profile before registering for events"

        return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})
    
    volunteer = Volunteer.objects.get(profile=profile)
    event = Event.objects.get(id=eventId)
    if event.noOfPositions != 0:
        volunteer.event.add(event)
        event.noOfPositions = event.noOfPositions-1
        event.save()
        message = "Registered for event " + event.eventName + " successfully."
    else:
        message = "You are late."

    return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})

def myEvents(request, username):
    profile = Profile.objects.get(userName = username)
    volunteer = Volunteer.objects.get(profile=profile)
    event = volunteer.event.all()

    return render(request, 'my_events.html', {'user_type': 1, 'events': event, 'username': username})

def unRegisterEvent(request, eventId, username):
    profile = Profile.objects.get(userName = username)
    volunteer = Volunteer.objects.get(profile=profile)
    event = Event.objects.get(id=eventId)
    volunteer.event.remove(event)
    event.noOfPositions = event.noOfPositions + 1
    event.save()

    message = "Unregistered for event " + event.eventName + " successfully."
    
    return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': Event.objects.all(), 'username': username})

def volunteerEvents(request, username):
    profile = Profile.objects.get(userName = username)
    organization = Organization.objects.get(profile=profile)
    events = Event.objects.filter(organization=organization)
    message = ""

    return render(request, 'voluteer_event.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})
    

def eventDetails(request, eventId, username):
    events = Event.objects.get(id=eventId)
    message = ""
    return render(request, 'eventdetail.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})