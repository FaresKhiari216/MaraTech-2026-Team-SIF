from django.shortcuts import render

def login(request):
    return render(request,'UserApp/login.html')


def register(request):
    return render(request,'UserApp/register.html')