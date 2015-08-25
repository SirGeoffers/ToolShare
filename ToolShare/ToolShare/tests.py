"""
tests.py
SUBJECT TO CHANGE
"""

from django.test import TestCase
from django.test.client import Client
from ToolShare.models import *

"""UC-01 Testing"""
class UserRegistrationTests(TestCase):
    """Test User Registration"""
		
    def setUp(self):
        self.client = Client()
        login = self.client.login(username='wsxasd', password='wsxasd')
        self.assertEqual(login, True)
		
    def test_verification(self):
        """Test information verification"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


"""UC-02 Testing"""
class ToolAdditionTests(TestCase):
    """Test Adding Tools"""
	
    def setUp(self):
        User.objects.create_user('bob')
        ShareZone.objects.create(zipcode=12345)
        Profile.objects.create(user=User.objects.get(username='bob'), address='123 st st', zone=ShareZone.objects.get(zipcode=1111))
        Location.objects.create(name='valhalla', owner=Profile.objects.get(address='123 st st'), address='valhalla ave', shed=True)
        Tool.objects.create(name='rake', available=True, location=Location.objects.get(name='valhalla'), condition='good')
	
    def test_add_tool(self):
        """Add tool"""
        assertEqual(newTool(description='rake of justice', tool=Tool.objects.get(name='rake'), owner=Profile.objects.get(address='123 st st')), True)
		
    def test_cancel_tool_add(self):
        """Cancel Process"""
		#PENDING
        
    def test_remove_tool(self):
        """Remove tool"""
		#PENDING

"""UC-03 Testing"""
class LocationChangeTests(TestCase):
    """Test Changing Tool Sharing Location"""

    def test_change_tool_location(self):
        """Test changing tool location"""
        #PENDING
        
    def test_change_unavailable_tool_location(self):
        """Test changing a tool's location that is unavailable"""
        #PENDING

"""UC-04 Testing"""
class AvailabilityChangeTests(TestCase):
    """Test Changing Availability of Tools"""
	
    def setUp(self):
        User.objects.create_user('bob')
		ShareZone.objects.create(zipcode=12345)
        Profile.objects.create(user=User.objects.get(username='bob'), address='123 st st', zone=Profile.objects.get(zipcode=12345))
        Location.objects.create(name='valhalla', owner=Profile.objects.get(address='123 st st'), address='valhalla ave', shed=True)
        Tool.objects.create(name='rake', available=True, location=Location.objects.get(name='valhalla'), condition='good')
	
    def test_change_to_available(self):
        """Change to Available"""
        tool = Tool.objects.get(name='rake')
        setattr(tool, 'available', True)
        self.assertEqual(tool.available, True)
		
    def test_change_to_unavailable(self):
        """Change to Unavailable"""
        tool = Tool.objects.get(name='rake')
        setattr(tool, 'available', False)
        self.assertEqual(tool.available, False)
		
"""UC-05 Testing"""
class BorrowRequestTests(TestCase):
    """Test Borrow Requests"""

    def setUp(self):
        Request.objects.create(description='me', tool=Tool.objects.get(name='Super Hammer'), owner=Profile.objects.get(address='123 Yes Court'))
        Request.objects.create(description='me', tool=Tool.objects.get(name='New Tool 1'), owner=Profile.objects.get(address='123 Yes Court'))
	
    def test_borrow_tool(self):
        """Borrow a valid tool"""
		assertEqual(borrow_request(Request.objects.get(description='me'), Tool.objects.get(name='New Tool 1')), True)
		
    def test_borrow_unavailable(self):
        """Attempt to borrow unavailable tool"""
		assertEqual(borrow_request(Request.objects.get(description='me'), Tool.objects.get(name='Super Hammer')), True)
		
    def test_borrow_request(self):
        """Send a borrow Request"""
        #PENDING
		
"""UC-06 Testing"""
class HandleBorrowTests(TestCase):
    """Test Handling Borrow Requests"""
	
	
    def test_accept_request(self):
        """Accept the request"""
		#PENDING
    def test_deny_request(self):
        """Deny the request"""
		#PENDING