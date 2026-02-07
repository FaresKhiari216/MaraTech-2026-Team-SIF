
from django.shortcuts import redirect, render
from EventApp.forms import EventForm, EventSearchForm
from .models import Event
from UserApp.models import Association


def _is_association_user(user):
    if not user.is_authenticated:
        return False
    return Association.objects.filter(user=user).exists()


def index_event(request):
    events = Event.objects.all()
    form = EventSearchForm()
    is_association = _is_association_user(request.user)
    context = {
        "events": events,
        "form": form,
        "logged_in_user": request.user,
        "is_association": is_association,
    }
    return render(request, "event.html", context)


def search_events(request):
    form = EventSearchForm(request.GET or None)
    events = Event.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("keywords")
        if query:
            events = events.filter(title__icontains=query) | events.filter(description__icontains=query)

    is_association = _is_association_user(request.user)
    context = {
        "search_events": events,
        "events": events,
        "form": form,
        "logged_in_user": request.user,
        "is_association": is_association,
    }
    return render(request, "event.html", context)

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.association = request.user.association
            event.save()
            return redirect("events:index")
    else:
        form = EventForm()

    return render(request, "eventApp/create_event.html", {"form": form})