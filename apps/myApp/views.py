from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..loginApp.models import User
from .models import Job
from django.contrib import messages

# CRUD

def  addToDB(title, description, location, id_user):

    job = Job.objects.create(
        title = title,
        description = description,
        location = location,
        job_posted_by = User.objects.get(id = id_user),
    )

    return job


def updateOnDB(title, description, location, id_job):

    print(description)
    print(location)

    job = Job.objects.get(id = id_job)
    job.title = title
    job.description = description
    job.location = location
    job.save()

    return job


def removeFromDB(id_job):
    
    job = Job.objects.get(id = id_job)
    job.delete()

    return True


def addToMyListDB(id_job,id_user):

    job = Job.objects.get(id = id_job)
    user = User.objects.get(id = id_user)

    job.job_taken_by = user
    job.save()

    return job



# ROUTES
def gotoDashboard(request):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    context = {
        'user' : User.objects.get(id = request.session['id']),
        'jobs' : Job.objects.filter(job_taken_by__isnull=True),
        #myjobs = user.taken_jobs.all
    }

    return render(request,'index.html',context)


def gotoAddJob(request):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    context = {
        'tipo' : 'add',
    }

    return render(request,'addOrEditJob.html',context) 

def createJob(request):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 

            job = Job(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
            )

            context = {
                'job' : job,
                'tipo' : 'add',
            }
            
            return render(request,'addOrEditJob.html',context) #go back to "addJob/create"

        else:

            job = addToDB(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
                id_user = request.session['id'],
            )

            messages.success(request, f"[Id.{job.id}] {job.title} successfully added to list of available jobs!")
    
    return redirect('dashboard')


def gotoEditJob(request,id_job):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    job = Job.objects.get(id = id_job)

    user = User.objects.get(id = request.session['id'])
    
    if user.id != job.job_posted_by.id:
        return redirect('dashboard')

    context = {
        'job' : job,
        'tipo' : 'edit',
    }
    
    return render(request,'addOrEditJob.html',context) 


def updateJob(request,id_job):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    job = Job.objects.get(id = id_job)

    if request.session['id'] != job.job_posted_by.id:
        return redirect('dashboard')    

    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value) 

            job = Job(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
                id = id_job,
            )

            context = {
                'job' : job,
                'tipo' : 'edit',
            }
            
            return render(request,'addOrEditJob.html',context) #go back to "addJob/create"

        else:

            job = updateOnDB(
                title = request.POST['title'],
                description = request.POST['description'],
                location = request.POST['location'],
                id_job = id_job,
            )

            messages.success(request, f"[Id.{job.id}] {job.title} successfully updated!")

            return redirect('dashboard')  
    


def viewJob(request,id_job):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    context = {
        'job' : Job.objects.get(id = id_job)
    }
    return render(request,'viewJob.html',context) 


def  addToMyJobs(request,id_job):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')
    
    if len(Job.objects.filter(id = id_job,job_taken_by__isnull = True)) > 0:
        id_user = request.session['id']
        job = addToMyListDB(id_job,id_user)
        messages.success(request, f"[Id.{job.id}] {job.title} successfully added to My List of Jobs!")

    return redirect('dashboard')


def deleteJob(request,id_job):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    job = Job.objects.get(id = id_job)
    job_title = job.title 

    if job.job_taken_by and job.job_taken_by.id == request.session['id']:
        removeFromDB(id_job)
        messages.success(request, f"[Id.{id_job}] {job_title} done and removed from My Jobs!")
    elif job.job_posted_by.id == request.session['id']:
        removeFromDB(id_job)
        messages.warning(request, f"[Id.{id_job}] {job_title} cancelled!")

    return redirect('dashboard')