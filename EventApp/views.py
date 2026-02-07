
from django.shortcuts import redirect, render
from EventApp.forms import EventForm
from .models import Event


def index_event(request):
    events = Event.objects.all()
    return render(request, "event.html", {"events": events})

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # Lier l'évènement à l'association de l'utilisateur connecté
            event = form.save(commit=False)
            event.association = request.user.association
            event.save()
            return redirect("events:index")
    else:
        form = EventForm()

    return render(request, "eventApp/create_event.html", {"form": form})