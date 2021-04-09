
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard', views.gotoDashboard, name='dashboard'),
    path('addJob',views.gotoAddJob,name='addjob'),
    path('addJob/create',views.createJob,name='createjob'),
    path('addToMyJobs/<int:id_job>',views.addToMyJobs,name='addtomyjobs'),
    path('view/<int:id_job>',views.viewJob,name='viewjob'),
    path('edit/<int:id_job>',views.gotoEditJob,name='editjob'),
    path('edit/<int:id_job>/update',views.updateJob,name='updatejob'),
    path('delete/<int:id_job>',views.deleteJob,name='deletejob'),
]