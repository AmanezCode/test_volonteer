from django.contrib import admin
from django.urls import path
from . import views
from . import v_controller
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index_view),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('setting/<int:userType>/<str:username>', v_controller.setting, name='setting'),
    path('update_setting/<str:username>', v_controller.updateOrgSetting, name='update_setting'),
    path('update_profile/<str:username>', v_controller.update_profile, name='update_profile'),
    path('event_creation/<str:username>/', v_controller.event_creation, name='event_creation'),
    path('deleteEvent/<int:eventId>/<str:username>/', v_controller.deleteEvent, name='deleteEvent'),
    path('loadHomepage/<str:username>/', v_controller.loadHomepage, name='loadHomepage'),
    path('registerEvent/<int:eventId>/<str:username>/', v_controller.registerEvent, name='registerEvent'),
    path('unRegisterEvent/<int:eventId>/<str:username>/', v_controller.unRegisterEvent, name='unRegisterEvent'),
    path('myEvents/<str:username>/', v_controller.myEvents, name='myEvents'),
    path('volunteerEvents/<str:username>/', v_controller.volunteerEvents, name='volunteerEvents'),
    path('logout/', views.logouts, name='logout'),
    path('event-details/<int:eventId>/<str:username>/', v_controller.eventDetails, name='eventDetails')
]

urlpatterns += staticfiles_urlpatterns()