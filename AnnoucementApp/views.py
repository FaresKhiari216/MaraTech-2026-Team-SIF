from django.shortcuts import render

def home(request):
    return render(request,'index.html')

def event(request):
    return render(request,'event.html')

def announcement(request):
    return render(request,'announcement.html')

