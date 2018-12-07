from django.http import HttpResponse

from django.shortcuts import render

def hello(request,SID=None):
    context = {};
    return render(request,"register.html",context)

