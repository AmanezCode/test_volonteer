from django.shortcuts import render
from .models import Profile, Organization, Event
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        firstName = request.POST['name']
        lastName = request.POST['lastname']
        userName = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        userType = request.POST['userType']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
                return redirect('signup')
            elif User.objects.filter(username=userName).exists():
                messages.info(request, 'username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=userName, email=email, password=password)
                user.save()

                userProfile = Profile(firstName=firstName, lastName=lastName, userType=userType, userName=user)
                userProfile.save()

                return redirect('/login/')
        else:
            messages.info(request, "passwords do not match")
            return redirect('signup/')
            
    return render(request, "registrationapp/signup.html")

def index_view(request):
    return render(request, 'index.php')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            message = "login successful"
            profile = Profile.objects.get(userName=username)
            allEvents = []
            if profile.userType==1:
                events = Event.objects.all()
                return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})
            else:
                try:
                    organization = Organization.objects.get(profile=profile)
                    allEvents = Event.objects.filter(organization = organization)
                    print(allEvents)
                except:
                    organization = ""
                
                return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})
            
        else:
            message = "Invalid username or password"
            return render(request, 'registrationapp/login.html', {'message': message})
    else:
        return render(request, 'registrationapp/login.html')

def logouts(request):
    logout(request)
    return redirect('/')
