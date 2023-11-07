from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE, default=None)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    ch = [(0,'-----'), (1,'Volunteer'), (2,'Organizer')]
    userType = models.PositiveIntegerField(choices=ch, default=0)
    def __str__(self):
        return self.firstname

class Organization(models.Model):
    orgName = models.CharField(max_length=50)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    orgDivision = models.CharField(max_length=50)
    orgRating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.orgName

class Event(models.Model):
    eventName = models.CharField(max_length=100)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    eventDescription = models.CharField(max_length=400)
    eventType = models.CharField(max_length=50)
    noOfPositions = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=400, null=True)
    eventDate = models.DateField(auto_now_add=False, null=True)
    startTime = models.CharField(max_length=400, null=True)
    endTime = models.CharField(max_length=400, null=True)

    def __str__(self):
        return self.eventName

class Volunteer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ManyToManyField(Event)
    skills = models.CharField(max_length=500)
    highLevelEducation = models.CharField(max_length=30)

    def __str__(self):
        return self.profile.username.username