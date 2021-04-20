from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import *
from .filters import ValidVisitorFilter
from .forms import *


def landing_page(request):
    return render(request, 'accounts/landing.html')

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if Society.objects.filter(user=user).exists():
                socinfo = Society.objects.get(user=user)
                url = "/dashboard/{}/".format(str(socinfo.id))
                return redirect(url)
            else:
                return redirect('socdetails')
        

    
    return render(request, 'accounts/login.html', context)

def register_view(request):
    context = {}
    
    form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for '+ user)

        return redirect('login')
    context['form'] = form
    
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('landingpage')

@login_required(login_url='login')
def regsociety(request):
    context = {}
    
    user = request.user
    if Society.objects.filter(user=user).exists():
        socinfo = Society.objects.get(user=user)
        url = "/dashboard/{}/".format(str(socinfo.id))
        return redirect(url)
    
    context['user'] = user
    
    form = CreateSocietyForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Society was created for '+ user)

        socinfo = Society.objects.get(user=user)
        url = "/dashboard/{}/".format(str(socinfo.id))
        return redirect(url)
    else:
        messages.info(request, 'Please enter all the details correctly')
    context['form'] = form
    return render(request, 'accounts/details.html', context)

@login_required(login_url='login')
def home(request, pk):
    context = {}

    user = request.user

    socinfo = Society.objects.get(id=pk)

    context['socinfo'] = socinfo

    validvisitors = ValidVisitor.objects.filter(soc_name_id=pk).order_by('entry_date', 'entry_time').reverse()[:2]
    
    curdate = datetime.today().date()
    visitorstoday = ValidVisitor.objects.filter(soc_name_id=pk, entry_date=curdate).count()
    newvisitor = NewVisitor.objects.filter(soc_name_id=pk).count()
    nomasktoday = InvalidVisitor.objects.filter(soc_name_id=pk, entry_date=curdate, status="No Mask").count()
    temptoday = InvalidVisitor.objects.filter(soc_name_id=pk, entry_date=curdate, status="High Temperature").count()

    context = {
        'socinfo'       : socinfo, 
        'visitorstoday' : visitorstoday,
        'validvisitors' : validvisitors,
        'newvisitor'    : newvisitor, 
        'nomasktoday'   : nomasktoday,
        'temptoday'     : temptoday
        }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def visitors(request, pk):
    context = {}
    socinfo = Society.objects.get(id=pk)
    validvisitors = ValidVisitor.objects.all().order_by('entry_date', 'entry_time').reverse()
    invalidvisitors = InvalidVisitor.objects.all().order_by('entry_date', 'entry_time').reverse()

    myFilter = ValidVisitorFilter(request.GET, queryset=validvisitors)
    validvisitors = myFilter.qs

    context = {
        'socinfo': socinfo, 
        'validvisitors': validvisitors, 
        'invalidvisitors': invalidvisitors,
        'myFilter': myFilter
        }

    return render(request, 'accounts/visitors.html', context)

@login_required(login_url='login')
def society(request, pk):
    context = {}
    socinfo = Society.objects.get(id=pk)
    context['socinfo'] = socinfo

    return render(request, 'accounts/society.html', context)

def validvisitorentry(request, pk, *args, **kwargs):
    context = {}
    socinfo = Society.objects.get(id=pk)
    context['socinfo'] = socinfo
    if request.method == 'GET':
        
        vname   = request.GET.get('name')
        visitor = ValidVisitor.objects.create(
                name        = vname, 
                entry_date  = request.GET.get('entry_date'),
                entry_time  = request.GET.get('entry_time'),
                temp        = request.GET.get('temp'),
                soc_name_id = pk
                )
        history = ValidVisitor.objects.filter(name=vname).count()
        if history <= 1:
            newvisitor = NewVisitor.objects.create(
                name        = vname,
                soc_name_id = pk
            )
        elif history > 1:
            newvisitor = NewVisitor.objects.filter(
                name        = vname,
                soc_name_id = pk
            ).delete()
        
    return HttpResponse('Done')

def invalidvisitorentry(request, pk, *args, **kwargs):
    context = {}

    socinfo = Society.objects.get(id=pk)
    context['socinfo'] = socinfo
    if request.method == 'GET':

        visitor = InvalidVisitor.objects.create(
                name        = request.GET.get('name'), 
                entry_date  = request.GET.get('entry_date'),
                entry_time  = request.GET.get('entry_time'),
                temp        = request.GET.get('temp'),
                status      = request.GET.get('status'),
                soc_name_id = pk
                )
    return HttpResponse('Done')