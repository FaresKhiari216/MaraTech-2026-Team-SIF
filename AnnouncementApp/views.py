from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from UserApp.models import Association
from .models import Announcement, Donation
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
        association = form.cleaned_data.get("association")

        if category:
            results = results.filter(category=category)
        if keywords:
            results = results.filter(title__icontains=keywords) | results.filter(description__icontains=keywords)
        if association:
            results = results.filter(association=association)
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
            association = Association.objects.filter(user=request.user).first()
            if association:
                annoucement.association = association
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
    is_owner = False
    if request.user.is_authenticated:
        association = Association.objects.filter(user=request.user).first()
        if association is not None:
            is_association = True
            if announcement_content.association == association:
                is_owner = True
    return render(
        request,
        "announcement/Details_Announcement.html",
        {
            "announcement": announcement_content,
            "is_association": is_association,
            "is_owner": is_owner,
        },
    )

@login_required
def edit_announcement(request, announcement_id):
    announcement = Announcement.objects.get(pk=announcement_id)

    # Vérifier que l'utilisateur est bien l'association créatrice de l'annonce
    association = Association.objects.filter(user=request.user).first()
    if association is None or announcement.association != association:
        return redirect("announcements:index")

    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect("announcements:Details_Announcement", announcement_id=announcement.id)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, "announcement/edit_announcement.html", {"form": form, "announcement": announcement})


@login_required
def delete_announcement(request, announcement_id):
    announcement = Announcement.objects.get(pk = announcement_id)

    # Vérifier que l'utilisateur est bien l'association créatrice de l'annonce
    association = Association.objects.filter(user=request.user).first()
    if association is None or announcement.association != association:
        return redirect('announcements:index')

    announcement.delete()
    return redirect('announcements:index')


def donate_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    if not request.user.is_authenticated:
        return redirect('login')

    Donation.objects.create(donateur=request.user, announcement=announcement)

    if announcement.link:
        return redirect(announcement.link)

    return redirect('announcements:Details_Announcement', announcement_id=announcement.id)

