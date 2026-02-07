from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import User, Association


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