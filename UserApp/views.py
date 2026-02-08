from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDate, TruncMonth, ExtractHour, ExtractDay
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from datetime import date
import calendar
from .models import User, Association
from EventApp.models import Event, EventFollow
from AnnouncementApp.models import Announcement, Donation


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

            
            auth_login(request, user)
            return redirect('login')
    else:
        errors = []

    return render(request, 'UserApp/register.html', {'errors': errors})


def logout(request):
	auth_logout(request)
	return redirect('login')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            # Bloquer l'accès si l'association liée n'est pas encore vérifiée
            association = Association.objects.filter(user=user).first()
            if association and not association.is_verified:
                error = "Votre association est en cours de validation par un administrateur."
                return render(request, 'UserApp/login.html', {'error': error})

            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_stats')
            return redirect('index')
        else:
            error = "Email ou mot de passe incorrect."
            return render(request, 'UserApp/login.html', {'error': error})
    return render(request, 'UserApp/login.html')


def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        user = User.objects.filter(email=email).first()
        # On ne révèle pas si l'email existe ou non
        if user:
            token_generator = PasswordResetTokenGenerator()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', args=[uidb64, token])
            )

            try:
                send_mail(
                    subject="Réinitialisation de votre mot de passe Seenedni",
                    message=(
                        f"Bonjour {user.first_name},\n\n"
                        "Vous avez demandé à réinitialiser votre mot de passe Seenedni.\n"
                        f"Cliquez sur le lien suivant pour définir un nouveau mot de passe :\n{reset_link}\n\n"
                        "Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email."
                    ),
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                pass

        return render(request, 'UserApp/password_reset_request_done.html')

    return render(request, 'UserApp/password_reset_request.html')


def password_reset_confirm(request, uidb64, token):
    token_generator = PasswordResetTokenGenerator()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not token_generator.check_token(user, token):
        return render(request, 'UserApp/password_reset_invalid.html')

    error = None
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not password1 or password1 != password2:
            error = "Les mots de passe ne correspondent pas."
        else:
            user.set_password(password1)
            user.save()
            return redirect('login')

    context = {'error': error}
    return render(request, 'UserApp/password_reset_confirm.html', context)


@login_required
def profile(request):
    user = request.user

    association = Association.objects.filter(user=user).first()
    is_association = association is not None

    events_participating = []
    stats = {}

    if is_association:
        total_events = Event.objects.filter(association=association).count()
        total_announcements = Announcement.objects.filter(association=association).count()
        reached_announcements = Announcement.objects.filter(
            association=association,
            current_amount__gte=F("target_amount"),
        ).count()

        stats = {
            "total_events": total_events,
            "total_announcements": total_announcements,
            "reached_announcements": reached_announcements,
        }
    else:
        events_participating = (
            EventFollow.objects.filter(user=user)
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


@login_required
def admin_stats(request):
    # Seuls les superutilisateurs ont accès à cette page
    if not request.user.is_superuser:
        return redirect('index')

    period = request.GET.get('period', 'daily')  # 'daily' ou 'monthly'

    today = date.today()
    qs = Donation.objects.all()

    if period == 'monthly':
        year = today.year
        month = today.month
        days_in_month = calendar.monthrange(year, month)[1]

        monthly_qs = qs.filter(created_at__year=year, created_at__month=month)
        aggregated = (
            monthly_qs.annotate(day=ExtractDay('created_at'))
            .values('day')
            .annotate(total_donations=Count('id'))
        )
        counts_by_day = {entry['day']: entry['total_donations'] for entry in aggregated}

        labels = [str(d) for d in range(1, days_in_month + 1)]
        data = [counts_by_day.get(d, 0) for d in range(1, days_in_month + 1)]
    else:
        period = 'daily'
        daily_qs = qs.filter(created_at__date=today)
        aggregated = (
            daily_qs.annotate(hour=ExtractHour('created_at'))
            .values('hour')
            .annotate(total_donations=Count('id'))
        )
        counts_by_hour = {entry['hour']: entry['total_donations'] for entry in aggregated}

        labels = [f"{h}h" for h in range(24)]
        data = [counts_by_hour.get(h, 0) for h in range(24)]

    stats = {
        'total_users': User.objects.count(),
        'total_associations': Association.objects.count(),
        'total_announcements': Announcement.objects.count(),
        'total_donations': Donation.objects.count(),
    }

    context = {
        'period': period,
        'labels': labels,
        'data': data,
        'stats': stats,
    }
    return render(request, 'UserApp/admin_stats.html', context)


@login_required
def admin_stat_doss_asso(request):
    # Page de gestion des associations en attente de vérification, réservée aux superadmins
    if not request.user.is_superuser:
        return redirect('index')

    if request.method == 'POST':
        association_id = request.POST.get('association_id')
        if association_id:
            association = Association.objects.filter(id=association_id, is_verified=False).first()
            if association:
                association.is_verified = True
                association.save()
                # Envoyer un email à l'association pour l'informer de la validation
                try:
                    send_mail(
                        subject="Validation de votre association sur Seenedni",
                        message=(
                            f"Bonjour {association.user.first_name},\n\n"
                            f"Votre association '{association.name}' a été validée par un administrateur Seenedni.\n"
                            f"Vous pouvez maintenant vous connecter et commencer à publier vos annonces.\n\n"
                            "Merci pour votre engagement."
                        ),
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                        recipient_list=[association.email],
                        fail_silently=True,
                    )
                except Exception:
                    # On ignore les erreurs d'envoi pour ne pas bloquer la validation
                    pass
        return redirect('admin_stat_doss_asso')

    pending_associations = Association.objects.filter(is_verified=False).select_related('user')

    context = {
        'pending_associations': pending_associations,
    }
    return render(request, 'UserApp/admin_stat_doss_asso.html', context)