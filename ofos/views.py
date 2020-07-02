from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse

def land(request):
    return render(request,'food/landing.html')