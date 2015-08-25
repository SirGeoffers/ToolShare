from django.db import models
from django.contrib.auth.models import *

class ShareZone(models.Model):

    zipcode = models.IntegerField("Zip Code")

    def __str__(self):
        return "Zone: " + str(self.zipcode)

class Profile(models.Model):
    """ Contains the information and functionality of the user that is not auth-related """
    
    user = models.OneToOneField(User, related_name='profile')
    address = models.TextField("Address", blank=True)
    phone = models.CharField("Phone Number", max_length=30, blank=True)
    zone = models.ForeignKey(ShareZone)

    def __str__(self):
        return "Profile: " + self.user.username
    
    
class Location(models.Model):
    """ Contains the information and functionality of the location """

    name = models.CharField("Location Name", max_length=40, blank=True)
    address = models.TextField("Address", blank=True)
    #shed will be true is location is shed, and false if it is a home
    shed = models.BooleanField()
    owner = models.ForeignKey(Profile)
    zone = models.ForeignKey(ShareZone)

    def __str__(self):
        return "Location: " + self.name


class Tool(models.Model):
    """ Contains the information and functionality of the tool """

    name = models.CharField("Tool Name", max_length=50, blank=True)
    description = models.TextField("Description", blank=True, unique=True)
    condition = models.CharField("Condition", max_length=30, blank=True)
    available = models.BooleanField("Available")
    startdate = models.DateTimeField(blank=True, null=True)
    enddate = models.DateTimeField(blank=True, null=True)
    location = models.ForeignKey(Location)
    borrower = models.ForeignKey(Profile, blank=True, null=True, related_name="borrowed_tools")

    def __str__(self):
        return "Tool: " + self.name


class Request(models.Model):
    """ Contains the information and functionality of the request made for a tool """

    description = models.TextField("Request", blank=True)
    duedate = models.DateTimeField(auto_now_add=True)
    tool = models.ForeignKey(Tool)
    owner = models.ForeignKey(Profile)    
    




    
