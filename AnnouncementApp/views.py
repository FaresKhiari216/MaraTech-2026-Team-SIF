from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from UserApp.models import Association
from .models import Announcement
from .forms import AnnouncementForm, AnnouncementSearchForm


def index(request):
    announcements = Announcement.objects.all()
    form = AnnouncementSearchForm()
    is_association = False
    if request.user.is_authenticated:
        is_association = Association.objects.filter(user=request.user).exists()
    context = {
        "announcements": announcements,
        "form": form,
        "logged_in_user": request.user,
        "is_association": is_association,
    }
    return render(request, "announcement.html", context)

def search_announcements(request):
    form = AnnouncementSearchForm(request.GET or None)
    results = Announcement.objects.all()

    is_association = False
    if request.user.is_authenticated:
        is_association = Association.objects.filter(user=request.user).exists()

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

    return render(
        request,
        "announcement.html",
        {
            "form": form,
            "results_search": results,
            "Announcements": results,
            "logged_in_user": request.user,
            "is_association": is_association,
        },
    )


@login_required
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
    announcement_content = Announcement.objects.get(pk=announcement_id)
    announcement_content.views += 1
    announcement_content.save(update_fields=["views"])
    is_association = False
    if request.user.is_authenticated:
        is_association = Association.objects.filter(user=request.user).exists()
    return render(
        request,
        "announcement/Details_Announcement.html",
        {"announcement": announcement_content, "is_association": is_association},
    )

def edit_announcement(request, announcement_id):
    announcement = Announcement.objects.get(pk=announcement_id)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect("announcements:Details_Announcement", announcement_id=announcement.id)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "announcement/edit_announcement.html", {"form": form, "announcement": announcement})

def delete_announcement(request, announcement_id):
	announcement = Announcement.objects.get(pk = announcement_id)
	announcement.delete()
	return redirect('announcements:index')

