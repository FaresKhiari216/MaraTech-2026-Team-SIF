from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncMonth
from .models import User, Association
from EventApp.models import Event, EventFollow
from AnnouncementApp.models import Announcement


def login(request):
    return render(request, 'UserApp/login.html')


def register(request):
    if request.method == 'POST':
        account_type = request.POST.get('account_type', 'donor')
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        photo = request.FILES.get('photo')
        receipt = request.FILES.get('receipt')

        errors = []

        if not last_name:
            errors.append("Le nom est obligatoire.")
        if account_type == 'donor' and not first_name:
            errors.append("Le prénom est obligatoire pour un donateur.")
        if not email:
            errors.append("L'adresse e-mail est obligatoire.")
        if not password1 or not password2 or password1 != password2:
            errors.append("Les mots de passe ne correspondent pas.")
        if account_type == 'association' and not receipt:
            errors.append("Le document justificatif est obligatoire pour une association.")

        if not errors:
            # S'assurer que les champs obligatoires du modèle User sont remplis
            if not first_name:
                first_name_to_use = last_name or "Association"
            else:
                first_name_to_use = first_name
            last_name_to_use = last_name or first_name_to_use

            user = User.objects.create_user(
                email=email,
                first_name=first_name_to_use,
                last_name=last_name_to_use,
                password=password1,
            )
            if photo:
                user.photo = photo
                user.save()

            if account_type == 'association':
                Association.objects.create(
                    user=user,
                    name=last_name or email,
                    description="Association inscrite via le formulaire d'inscription.",
                    category="humanitary",
                    email=email,
                    photo=photo,
                    receipt=receipt,
                )

            # Connexion automatique après inscription
            auth_login(request, user)
            return redirect('index')
    else:
        errors = []

    return render(request, 'UserApp/register.html', {'errors': errors})


def logout(request):
	auth_logout(request)
	return redirect('login')

def login(request ) :
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            auth_login(request, user)
            return redirect('index')
        else:
            error = "Email ou mot de passe incorrect."
            return render(request, 'UserApp/login.html', {'error': error})
    return render(request, 'UserApp/login.html')


@login_required
def profile(request):
    user = request.user

    association = Association.objects.filter(user=user).first()
    is_association = association is not None

    events_participating = []
    stats = {}

    if is_association:
        events_qs = Event.objects.filter(association=association)
        announcements_qs = Announcement.objects.filter(association=association)

        total_events = events_qs.count()
        total_announcements = announcements_qs.count()
        reached_announcements = announcements_qs.filter(
            target_amount_achieved__exact=True,
        ).count()

        # Événements créés par mois (courbe)
        events_by_month_qs = (
            events_qs
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        events_by_month_labels = [e["month"].strftime("%b %Y") for e in events_by_month_qs]
        events_by_month_counts = [e["count"] for e in events_by_month_qs]

        # Annonces créées par mois (courbe)
        announcements_by_month_qs = (
            announcements_qs
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(count=Count("id"))
            .order_by("month")
        )

        announcements_by_month_labels = [a["month"].strftime("%b %Y") for a in announcements_by_month_qs]
        announcements_by_month_counts = [a["count"] for a in announcements_by_month_qs]

        # Annonces financées par catégorie (barplot)
        category_display = dict(Announcement.CATEGORY_CHOICES)
        financed_by_category_qs = (
            announcements_qs
            .filter(target_amount_achieved__exact=True)
            .values("category")
            .annotate(count=Count("id"))
            .order_by("category")
        )

        financed_by_category_labels = [category_display.get(a["category"], a["category"]) for a in financed_by_category_qs]
        financed_by_category_counts = [a["count"] for a in financed_by_category_qs]

        stats = {
            "total_events": total_events,
            "total_announcements": total_announcements,
            "reached_announcements": reached_announcements,
            "events_by_month_labels": events_by_month_labels,
            "events_by_month_counts": events_by_month_counts,
            "announcements_by_month_labels": announcements_by_month_labels,
            "announcements_by_month_counts": announcements_by_month_counts,
            "financed_by_category_labels": financed_by_category_labels,
            "financed_by_category_counts": financed_by_category_counts,
        }
    else:
        events_participating = (
            EventFollow.objects
            .filter(user=user)
            .exclude(event__status="cancelled")
            .select_related("event", "event__association")
            .order_by("-created_at")
        )

    context = {
        "user_obj": user,
        "association": association,
        "is_association": is_association,
        "events_participating": events_participating,
        "stats": stats,
    }
    return render(request, "UserApp/profile.html", context)