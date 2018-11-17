from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    ##takes user to login and registraton page

    url(r'^dashboard$', views.dashboard),
    ##takes user to the dashboard "the home"

    url(r'^login$', views.login),
    ##processes the login(email+pw) to get to the dashboard

    url(r'^registrationprocess$', views.registrationprocess, name="registration"),
    #registeration processing with entered information

    url(r'^logout$', views.logout),
    #clears out session for logged in user

    url(r'^jobs/new$', views.createJobs),
    #takes user to create job page

    url(r'^jobprocessing$', views.jobprocessing),
    #process the information of the newly created job and insert into database

    url(r'^jobs/edit/(?P<id>\d+)$', views.editpage),
    #renders the page for edit jobs

    url(r'^jobeditprocessing/(?P<id>\d+)$', views.jobeditprocessing),
    #starts to process the update changes to the job when submitted

    url(r'^jobs/(?P<id>\d+)$', views.jobprofile),
    #renders the page for job profile

    url(r'^deletejob/(?P<id>\d+)$', views.deletejob),
    #deletes the job from the database

    url(r'^addjob/(?P<id>\d+)$', views.addjob),
    #updates the database to add the job to the user

    url(r'^giveupjob/(?P<id>\d+)$', views.giveupjob),
    #can reference to deletejob when completed to remove this portion
]
