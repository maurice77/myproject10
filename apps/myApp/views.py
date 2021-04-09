from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..loginApp.models import User
#from .models import Job
from django.contrib import messages

# CRUD


# ROUTES
def gotoDashboard(request):

    if not 'id' in request.session or request.session['id'] == 0:
        return redirect('signin')

    context = {
        'user' : User.objects.get(id = request.session['id']),
    }

    return render(request,'index.html',context)

