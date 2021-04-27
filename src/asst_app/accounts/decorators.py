from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Society

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and Society.objects.filter(user=request.user).exists():
            soc = Society.objects.get(user=request.user)
            return redirect('../dashboard/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func