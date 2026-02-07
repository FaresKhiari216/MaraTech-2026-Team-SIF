from django.shortcuts import render, redirect
from .models import Announcement
from .forms import AnnouncementForm, AnnouncementSearchForm

def index(request):
	context = {"Announcements" : Announcement.objects.all()}
	return render(request, "announcement.html", context)

def search_announcements(request):
    form = AnnouncementSearchForm(request.GET or None)
    results = Announcement.objects.all()

    if form.is_valid():
        category = form.cleaned_data.get("category")
        keywords = form.cleaned_data.get("keywords")
        emergency = form.cleaned_data.get("emergency")

        if category:
            results = results.filter(category=category)
        if keywords:
            results = results.filter(title__icontains=keywords) | results.filter(description__icontains=keywords)
        if emergency:
            results = results.filter(emergency=True)

    return render(request, "announcement/search_results.html", {"form": form, "results": results})

def new_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            annoucement = form.save(commit=False)
            annoucement.user = request.user
            annoucement.save()
            return redirect('announcements:index')
    else:
        form = AnnouncementForm()

    return render(request, "announcement/create_announcement.html", {"form": form})

def details_announcement(request, announcement_id):
	announcement_content = Announcement.objects.get(pk = announcement_id)
	return render(request, "announcement/Details_Announcement.html", {"announcement":announcement_content})

def edit_announcement(request, announcement_id):
	announcement = Announcement.objects.get(pk = announcement_id)
	if request.method == 'POST':
		form = AnnouncementForm(request.POST, instance=announcement, user=request.user)

		if (form.is_valid()):
			form.save()
			return redirect('announcements:details_announcement', announcement_id=announcement.id)
	else:
		form = AnnouncementForm(instance=announcement, user=request.user)
	return render(request, "announcement/Edit_Announcement.html", {"announcement_object": announcement, "announcement":form, "announcement_id": announcement})

def delete_announcement(request, announcement_id):
	announcement = Announcement.objects.get(pk = announcement_id, user=request.user)
	announcement.delete()
	return redirect('announcements:index')

