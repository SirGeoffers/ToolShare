from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin, auth

admin.autodiscover()

urlpatterns = patterns('',
    # (?P<uid>\w+)
    url(r'^admin/', include(admin.site.urls)),
                       
    url(r'^$', 'ToolShare.views.home', name='home'),

    url(r'^inventory/?$', 'ToolShare.views.inventory', name='inventory'),
    url(r'^locations/?$', 'ToolShare.views.locations', name='locations'),
    url(r'^profile/?$', 'ToolShare.views.profile', name='profile'),
    url(r'^about/?$', 'ToolShare.views.about', name='about'),
	
    url(r'^register/?$', 'ToolShare.views.register', name='register'),

    url(r'^tool/new/$', 'ToolShare.views.newTool', name='newtool'),
    url(r'^tool/edit/(?P<toolid>\w+)/$', 'ToolShare.views.editTool', name='edittool'),
    url(r'^tool/delete/(?P<toolid>\w+)/$', 'ToolShare.views.deleteTool', name='deletetool'),
    url(r'^tool/return/(?P<toolid>\w+)/$', 'ToolShare.views.returnTool', name='returntool'),
    url(r'^tool/(?P<toolid>\w+)/$', 'ToolShare.views.tool', name='tool'),
    url(r'^borrow_request/(?P<toolid>\w+)/$', 'ToolShare.views.borrow_request', name='borrow_request'),
    url(r'^borrow_request_submit/(?P<toolid>\w+)/$', 'ToolShare.views.borrow_request_submit', name='borrow_request_submit'),
    url(r'^tool_request/(?P<toolid>\w+)/(?P<uid>\w+)/(?P<answer>\w+)/(?P<rid>\w+)/$', 'ToolShare.views.tool_request', name='tool_request'),

    url(r'^locations/new/$', 'ToolShare.views.newLocation', name='newlocation'),
	
	url(r'^profile/edit/$', 'ToolShare.views.editProfile', name='editprofile'),

    url(r'^login/$', 'django.contrib.auth.views.login',name="my_login"),
    url(r'^[^..]*login/[^..]*$', 'django.contrib.auth.views.login',name="my_login"),
    url(r'^[^..]*logout/[^..]*$', 'ToolShare.views.logout_view', name='logout' ),
    url(r'^accounts/profile/$', 'ToolShare.views.inventory', name='profileRedirect' ),
    url(r'^searchTool/(?P<query>\w+)/$', 'ToolShare.views.searchTool', name='searchTool' ),
	url(r'^SearchTool=(?P<query>\w+)/$', 'ToolShare.views.searchToolRedirect', name='searchToolRedirect'),
	#url(r'^[^..]*$', 'ToolShare.views.notFound',name="notFound"),
    


)
