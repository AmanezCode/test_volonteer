from django.shortcuts import render
from .models import Profile, Organization, Event
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout

def signup(request):
    if request.method == 'POST':
        firstname = request.POST['name']
        lastname = request.POST['lastname']
        username = request.POST['username'].lower()
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        userType = request.POST['userType']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Почта уже занята')

                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Юзернейм уже занят')

                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                userProfile = Profile(firstname=firstname, lastname=lastname, userType=userType, username=user)
                userProfile.save()

                return redirect('/login/')
        else:
            messages.info(request, "Пароли не совпадают")

            return redirect('signup/')
            
    return render(request, "registrationapp/signup.html")

def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username.lower(), password=password)
        
        if user is not None:
            message = "Успешный вход"
            profile = Profile.objects.get(username=username)
            allEvents = []
            if profile.userType == 1:
                events = Event.objects.all()
                return render(request, 'homepage.html', {'message': message, 'user_type': 1, 'events': events, 'username': username})
            else:
                try:
                    organization = Organization.objects.get(profile=profile)
                    allEvents = Event.objects.filter(organization = organization)
                except:
                    organization = ""
                
                return render(request, 'homepage.html', {'message': message, 'user_type': 2, 'organization': organization, 'events': allEvents, 'username': username})
        else:
            message = "Неправильный логин или пароль"
            return render(request, 'registrationapp/login.html', {'message': message})
    else:
        return render(request, 'registrationapp/login.html')

def logouts(request):
    logout(request)
    return redirect('/')