from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.db.models import Avg

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import *
from .forms import *
from .filters import ValidVisitorFilter
from .decorators import unauthenticated_user

from rest_framework.views import APIView
from rest_framework.response import Response

from datetime import datetime
from qrcode import *
import mimetypes

def landing_page(request):
    return render(request, 'landing.html')

def generateqr(request):
    context = {}
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        qr_data = str(fname)+'-'+str(lname)
        img = make(qr_data)
        qrpath = settings.MEDIA_ROOT+'/{}.png'.format(qr_data)
        img.save(qrpath)
        context = {
            'qr_data' : qr_data,
            'qrpath' : qrpath, 
        }
    return render(request, 'qr.html', context)

def dloadqr(request, name):
    imgpath      = settings.MEDIA_ROOT+'/{}.png'.format(name)
    filename = '{}.png'.format(name)
    fl = open(imgpath, 'rb')
    mime_type, _ = mimetypes.guess_type(imgpath)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    try:
        return response
    except Exception:
        HttpResponse("ERROR")

@unauthenticated_user
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
                url = "/dashboard/"
                return redirect(url)
            else:
                return redirect('socdetails')
    
    return render(request, 'accounts/login.html', context)

@unauthenticated_user
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

@login_required(login_url='landingpage')
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

# Send data through REST to charts.js
class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, pk, format=None):
        
        labels = []
        chartLabel = "visitor data"
        chartdata = []
        anotherdata = []
        pk = pk
        # soc = Society.objects.filter(user=user.id)
        
        tod = datetime.today().date()
        n = 6
        for i in range(0, n):
            noofdays = n-i
            that_date = tod - timedelta(days=noofdays)
            labels.append(str(that_date.strftime("%d %b")))
            visitor = ValidVisitor.objects.filter(soc_name_id=pk, entry_date=that_date)
            if visitor.exists():
                chartdata.append(visitor.count())
            else:
                chartdata.append(0)
            denied = InvalidVisitor.objects.filter(soc_name_id=pk, entry_date=that_date)
            if denied.exists():
                anotherdata.append(denied.count())
            else:
                anotherdata.append(0)
        
        
        d = tod.strftime("%d %b")
        labels.append(d)
        visitor = ValidVisitor.objects.filter(soc_name_id=pk, entry_date=tod)
        if visitor.exists():
            chartdata.append(visitor.count())
        else:
            chartdata.append(0)
        denied = InvalidVisitor.objects.filter(soc_name_id=pk, entry_date=tod)
        if denied.exists():
            anotherdata.append(denied.count())
        else:
            anotherdata.append(0)

        data = {
            'labels': labels,
            'chartLabel':chartLabel,
            'chartdata' : chartdata,
            'anotherdata':anotherdata,
            'pk':pk,
        }
        return Response(data)


# Main Dashboard
@login_required(login_url='login')
def home(request):
    context = {}

    user = request.user
    curdate = datetime.today().date()
    socinfo = Society.objects.get(user=user)
    context['socinfo'] = socinfo

    latestvisitors = ValidVisitor.objects.filter(soc_name_id=socinfo.id).order_by('entry_date', 'entry_time').reverse()[:5]    
    visitorstoday = ValidVisitor.objects.filter(soc_name_id=socinfo.id, entry_date=curdate)
    newvisitor = NewVisitor.objects.filter(soc_name_id=socinfo.id)
    nomasktoday = InvalidVisitor.objects.filter(soc_name_id=socinfo.id, entry_date=curdate, status="No Mask")
    temptoday = InvalidVisitor.objects.filter(soc_name_id=socinfo.id, entry_date=curdate, status="High Temperature")
    now = curdate.strftime("%d %b, %Y")

    
    total = visitorstoday.count()+nomasktoday.count()+temptoday.count()
    if total > 0:
        percentvalid = (visitorstoday.count()/total)*100
        percentinvalid = ((total-visitorstoday.count())/total)*100
        avgtemp = visitorstoday.aggregate(Avg('temp'))
        context['stats'] = 'True'
    
    if request.POST:
        invalidvisitorstoday = InvalidVisitor.objects.filter(soc_name_id=socinfo.id, entry_date=curdate)
        context = {
        'socinfo'             : socinfo, 
        'visitorstoday'       : visitorstoday,
        'newvisitor'          : newvisitor, 
        'invalidvisitorstoday': invalidvisitorstoday,
        'today'               : now,
        'total'               : total,
        'avgtemp'       : avgtemp['temp__avg'],
        'percentvalid'  : format(percentvalid, '.2f'),
        'percentinvalid': format(percentinvalid, '.2f'),
        }
        subject = 'Visitor Details of {}'.format(now)
        html_message = render_to_string('accounts/snippets/report.html', context)
        plain_message = strip_tags(html_message)
        from_email = 'From <donotreplyreport@securotech.com>'
        to = [user.email, ]
        msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
        msg.attach_alternative(html_message, "text/html")
        msg.send()

    context = {
        'socinfo'       : socinfo, 
        'visitorstoday' : visitorstoday,
        'latestvisitors': latestvisitors,
        'newvisitor'    : newvisitor, 
        'nomasktoday'   : nomasktoday,
        'temptoday'     : temptoday,
        'today'         : now,
        'avgtemp'       : avgtemp['temp__avg'],
        'percentvalid'  : format(percentvalid, '.2f'),
        'percentinvalid': format(percentinvalid, '.2f'),
        }
    
    return render(request, 'accounts/dashboard.html', context)

# #Send report:
# @login_required(login_url='login')
# def send_report(request):
#     context = {}
#     curdate = datetime.today().date()
#     user = request.user
#     soc  = Society.objects.get(user=user)
    
    


#detailed visitor view
@login_required(login_url='login')
def visitors(request):
    context = {}
    user = request.user

    socinfo = Society.objects.get(user=user)
    validvisitors = ValidVisitor.objects.all().order_by('entry_date', 'entry_time').reverse()
    invalidvisitors = InvalidVisitor.objects.all().order_by('entry_date', 'entry_time').reverse()

    myFilter = ValidVisitorFilter(request.GET, queryset=validvisitors)
    validvisitors = myFilter.qs

    context = {
        'socinfo'           : socinfo, 
        'validvisitors'     : validvisitors, 
        'invalidvisitors'   : invalidvisitors,
        'myFilter'          : myFilter,
        }

    return render(request, 'accounts/visitors.html', context)

# soc general info
@login_required(login_url='login')
def society(request):
    context = {}
    user = request.user
    socinfo = Society.objects.get(user=user)
    context['socinfo'] = socinfo
    form = EditSocietyInfoForm(request.POST)
    if request.POST:
        form = EditSocietyInfoForm(initial = {
                'name': socinfo.name,
                'sec_name': socinfo.sec_name,
            })
        if form.is_valid:
            form.save()
    
    context['form'] = form

    return render(request, 'accounts/society.html', context)



# entering validVisitor into db
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


# entering InvalidVisitor into db
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