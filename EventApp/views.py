
from django.shortcuts import redirect, render
from django.db.models import Exists, OuterRef
from django.contrib.auth.decorators import login_required
from EventApp.forms import EventForm, EventSearchForm
from .models import Event, EventFollow
from UserApp.models import Association


def _is_association_user(user):
    if not user.is_authenticated:
        return False
    return Association.objects.filter(user=user).exists()


def _is_normal_user(user):
    if not user.is_authenticated:
        return False
    return not _is_association_user(user)


def index_event(request):
    events = Event.objects.all()
    if request.user.is_authenticated:
        events = events.annotate(
            user_joined=Exists(
                EventFollow.objects.filter(user=request.user, event=OuterRef("pk"))
            )
        )
    form = EventSearchForm()
    is_association = _is_association_user(request.user)
    is_normal_user = _is_normal_user(request.user)
    context = {
        "events": events,
        "form": form,
        "logged_in_user": request.user,
        "is_association": is_association,
        "is_normal_user": is_normal_user,
    }
    return render(request, "event.html", context)


def search_events(request):
    form = EventSearchForm(request.GET or None)
    events = Event.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("keywords")
        association = form.cleaned_data.get("association")
        if query:
            events = events.filter(title__icontains=query) | events.filter(description__icontains=query)
        if association:
            events = events.filter(association=association)

    if request.user.is_authenticated:
        events = events.annotate(
            user_joined=Exists(
                EventFollow.objects.filter(user=request.user, event=OuterRef("pk"))
            )
        )

    is_association = _is_association_user(request.user)
    is_normal_user = _is_normal_user(request.user)
    context = {
        "search_events": events,
        "events": events,
        "form": form,
        "logged_in_user": request.user,
        "is_association": is_association,
        "is_normal_user": is_normal_user,
    }
    return render(request, "event.html", context)


def details_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    is_association = _is_association_user(request.user)
    is_normal_user = _is_normal_user(request.user)
    has_joined = False
    is_owner = False
    if is_association:
        association = Association.objects.filter(user=request.user).first()
        if association is not None and event.association == association:
            is_owner = True
    if request.user.is_authenticated:
        has_joined = EventFollow.objects.filter(user=request.user, event=event).exists()
    context = {
        "event": event,
        "is_association": is_association,
        "is_normal_user": is_normal_user,
        "has_joined": has_joined,
        "is_owner": is_owner,
    }
    return render(request, "eventApp/Details_event.html", context)


@login_required
def join_event(request, event_id):
    if not _is_normal_user(request.user):
        return redirect("events:index")

    event = Event.objects.get(pk=event_id)

    if event.status == "cancelled":
        return redirect("events:Details_event", event_id=event.id)

    EventFollow.objects.get_or_create(user=request.user, event=event)
    return redirect("events:Details_event", event_id=event.id)


@login_required
def cancel_event(request, event_id):
    if not _is_normal_user(request.user):
        return redirect("events:index")

    event = Event.objects.get(pk=event_id)
    EventFollow.objects.filter(user=request.user, event=event).delete()
    return redirect("events:Details_event", event_id=event.id)

@login_required
def create_event(request):
    if not _is_association_user(request.user):
        return redirect("events:index")

    association = Association.objects.filter(user=request.user).first()
    if association is None:
        return redirect("events:index")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.association = association
            event.save()
            return redirect("events:index")
    else:
        form = EventForm()

    return render(request, "eventApp/create_event.html", {"form": form})

@login_required
def edit_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    old_status = event.status

    # Vérifier que l'utilisateur est bien l'association créatrice de l'évènement
    association = Association.objects.filter(user=request.user).first()
    if association is None or event.association != association:
        return redirect("events:index")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated_event = form.save()
            # Si l'évènement vient d'être annulé, supprimer toutes les participations
            if old_status != "cancelled" and updated_event.status == "cancelled":
                EventFollow.objects.filter(event=updated_event).delete()
            return redirect("events:Details_event", event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "eventApp/edit_event.html", {"form": form, "event": event})


@login_required
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)

    # Vérifier que l'utilisateur est bien l'association créatrice de l'évènement
    association = Association.objects.filter(user=request.user).first()
    if association is None or event.association != association:
        return redirect("events:index")

    event.delete()
    return redirect("events:index")