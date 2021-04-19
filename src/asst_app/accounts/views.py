from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .models import *
from .filters import ValidVisitorFilter

def login(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def register(request):
    context = {}
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
    context['form'] = form

    return render(request, 'accounts/register.html', context)


def home(request, pk):
    context = {}
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