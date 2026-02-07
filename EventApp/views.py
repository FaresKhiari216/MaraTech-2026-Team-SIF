from django.shortcuts import render, redirect
from EventApp.models import Event
from .forms import EventForm

def index(request):
	context = {"events" : Event.objects.all()}
	return render(request, "event.html", context)

def search_event(request):
    query = request.GET.get("name_event")
    results = []

    if query:
        results = Event.objects.filter(title__icontains=query)

    return render(request, "event/search_results.html", {"results": results, "query": query})

def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('Events:index')
    else:
        form = EventForm()

    return render(request, "event/Add_Event.html", {"form": form})


def details_event(request, event_id):
	event_content = Event.objects.get(pk = event_id)
	return render(request, "event/Details_Event.html", {"event":event_content})

def edit_event(request, event_id):
	event = Event.objects.get(pk = event_id)
	if request.method == 'POST':
		form = EventForm(request.POST, instance=event, user=request.user)

		if (form.is_valid()):
			form.save()
			return redirect('Events:Details_Event', event_id=event.id)
	else:
		form = EventForm(instance=event, user=request.user)
	return render(request, "event/Edit_Event.html", {"event_object": event, "event":form, "event_id": event_id})

def delete_event(request, event_id):
	event = Event.objects.get(pk = event_id, user=request.user)
	event.delete()
	return redirect('Events:index')