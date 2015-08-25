from ToolShare.models import *
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as loginUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, \
    render_to_response
from django.core.urlresolvers import reverse
import datetime


def home(request):
    """ renders home page """	
    if request.GET and request.GET['SearchTool']!=None and request.GET['SearchTool']!='':
        return redirect("searchTool", query=request.GET['SearchTool'])
    return render(request, "ToolShare/pages/general/index.html", None)

def about(request):
    """ renders about page """
    return render(request, "ToolShare/pages/general/about.html", None)

@login_required
def inventory(request):
    """ renders inventory page """
    context = {
    "tools": Tool.objects.all()
    }
    return render(request, "ToolShare/pages/general/inventory.html", context)

@login_required
def locations(request):
    """ renders location page """
    context = {
    "locations": Location.objects.all(),
    "tools": Tool.objects.all()
    }
    return render(request, "ToolShare/pages/general/locations.html", context)

@login_required
def profile(request):
    """ renders profile page """
    context = {
    "locations": Location.objects.all(),
    "tools": Tool.objects.all(),
    "requests": Request.objects.all(),
    "error": request.GET["error"] if "error" in request.GET else None
    }

    return render(request, "ToolShare/pages/general/profile.html", context)
	
#@object_required(class_object=Tool, key="toolId")
@login_required
def tool(request, toolid):
    """ renders specific tool's page """
    this_tool =  get_object_or_404(Tool, pk=toolid)

    initial_date = datetime.date.today()
    if request.method == 'POST':
        if (not this_tool.location.shed):
            return redirect("/borrow_request/"+toolid)
        else:
            this_tool.borrower=Profile.objects.get(user=request.user)
            this_tool.save()

    context = {
    "tool": this_tool,
    "initial_date": "{}/{}/{}".format(initial_date.month, initial_date.day, initial_date.year)
    }
    return render(request, "ToolShare/pages/general/tool.html", context)

def borrow_request(request, toolid):
    """ renders form used to request a tool """
    context={"toolid": toolid}
    return render(request, "ToolShare/pages/general/borrow_request.html", context)

def borrow_request_submit(request, toolid):
    """ submits a request for a tool """
    description = request.POST["description"] if "description" in request.POST else ""
    initial_date = datetime.date.today()
    due_date = "{}/{}/{}".format(initial_date.year, initial_date.day, initial_date.month)
    tool = Tool.objects.get(id=toolid)
    prof = Profile.objects.get(user=request.user)
    Request.objects.create(description=description, tool=tool, owner=prof)

    return redirect("profile")

def tool_request(request, toolid, uid, answer, rid):
    """ control for either accepting or denying a tool request """
    this_tool =  get_object_or_404(Tool, pk=toolid)

    if answer == "1":
        this_tool.borrower=Profile.objects.get(id=uid)
        this_tool.save()
    Request.objects.get(id=rid).delete()

    return redirect("profile")

def login(request):        
    """ attempts to log in the user """
    return render_to_response("registration/login.html");

def notFound(request):
    """ renders 404 page """
    return render(request, "ToolShare/pages/error/404.html", None)

@login_required
def logout_view(request):
    """ attempts to log out the user """
    request.session.items = []
    request.session.modified = True
    logout(request)
    return redirect("home")

def register(request):
    """ attempts to register a user and create its corresponding objects in the database """
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        firstName = request.POST["first"]
        lastName = request.POST["last"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        zipcode = request.POST["zip"]
        if address=="" or address == None or phone == "" or phone == None or username=="" or password=="" or firstName=="" or lastName=="" or email=="" or username==None or password==None or firstName==None or lastName==None or email==None or zipcode=="":
            return HttpResponse("GO BACK AND ENTER ALL THE INFORMATION!") 
        else:
            if User.objects.filter(username=username).exists():
                return HttpResponse("THE USER ALREADY EXISTS DAMMIT!")
            userObject=User.objects.create_user(username, email=email, password=password, first_name=firstName, last_name=lastName)
            zones = ShareZone.objects.filter(zipcode=zipcode)
            if len(zones) == 0:
                zone = ShareZone.objects.create(zipcode=int(zipcode))
            else:
                zone = zones[0]
            prof = Profile.objects.create(user=userObject, address=address, phone=phone, zone=zone)
            Location.objects.create(name=username+"'s Shed", address=address, owner=prof, shed=False, zone=zone)
            user = authenticate(username=username, password=password)
            loginUser(request, user)
            return redirect("profile")
    else:
        return render(request, "registration/register.html")

@login_required
def newTool(request):
    """ attempts to create a new tool """
    if request.method == 'POST':
        toolName=request.POST["toolname"]
        description=request.POST["description"]
        condition=request.POST["condition"]
        location=request.POST["location"]
        if toolName=="" or toolName==None or description=="" or description==None or condition == "" or condition == None or location == "" or location == None:
            return HttpResponse("GO BACK AND ENTER ALL THE INFORMATION!") 
        else:
            Tool.objects.create(name=toolName, description=description, condition=condition, available=True, location=Location.objects.get(name=location))
            return redirect("profile")
        
    if not Location.objects.filter(owner=Profile.objects.get(user=request.user)).exists():
        redirect_url = reverse( "profile" )
        extra_params = '?error=10'
        return HttpResponseRedirect('%s%s' % (redirect_url, extra_params))
    return render(request, "ToolShare/pages/general/new_tool.html", {'locations': Location.objects.filter(owner=request.user.profile)})

def editTool(request, toolid):
    """ attempts to edit a tool """

    error = ""

    if request.POST:
        toolName=request.POST["toolname"]
        description=request.POST["description"]
        condition=request.POST["condition"]
        location=request.POST["location"]
        available=True if "available" in request.POST else False

        if not toolName or not description or not condition or not location:
            error = "Please fill out all of the fields."
        else:
            tool = Tool.objects.get(id=toolid)
            tool.name = toolName
            tool.description = description
            tool.condition = condition
            tool.location = Location.objects.get(name=location)
            tool.available = available
            tool.save()

            return redirect("tool", toolid=toolid)

    context = {
    "tool": get_object_or_404(Tool, id=toolid),
    "locations": Location.objects.filter(owner=request.user.profile),
    "error": error
    }
    return render(request, "ToolShare/pages/general/edit_tool.html", context)

def returnTool(request, toolid):
    """ returns a tool """

    tool = Tool.objects.get(id=toolid)
    tool.borrower = None
    tool.save()

    return redirect("tool", toolid=toolid)

def deleteTool(request, toolid):

    Tool.objects.get(id=toolid).delete()

    return redirect("profile")

def newLocation(request):
    """ attempts to create a new location """

    error = ""

    if request.POST:
        name=request.POST["locationname"]
        address=request.POST["address"]
        shed=True if "shed" in request.POST else False

        if not name or not address:
            error = "Please fill out all of the fields."
        else:
            Location.objects.create(owner=request.user.profile, name=name, address=address, shed=shed, zone=request.user.profile.zone)

            return redirect("profile")

    return render(request, "ToolShare/pages/general/new_location.html")

def editProfile(request):
    """ attempts to edit a profile """

    error = ""
    profile = Profile.objects.get(user=request.user)
    user = request.user
	
    if request.POST:
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        address=request.POST["address"]
        email=request.POST["email"]
        phone=request.POST["phone"]

        if not firstname or not lastname or not address or not email or not phone:
            error = "Please fill out all of the fields."
        else:
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            profile.address = address
            profile.phone = phone
            user.save()
            profile.save()

            return redirect("profile")

    context = {
    "profile": profile,
    "error": error
    }
    return render(request, "ToolShare/pages/general/edit_profile.html", context)	

@login_required
def searchTool(request, query):
    """ control for either accepting or denying a tool request """
	
    context = {
    "text": "Placeholder Text" 
    }
	
    return render(request, "ToolShare/pages/general/searchTool.html", context)
	
@login_required
def searchToolRedirect(request, query):
	""" redirects to the searchTool page """
	return redirect("searchTool", query)
