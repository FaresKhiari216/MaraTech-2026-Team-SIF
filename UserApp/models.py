from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Le champ email est obligatoire.")
        
        if password is None:
            raise ValueError("Le champ mot de passe est obligatoire.")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(
        upload_to="Profile_pictures/Donor/",
        default="Profile_pictures/default.jpg",
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

class Association(models.Model):
    ASSOCIATION_CATEGORY_CHOICES = [
        ("humanitary", "إِنْسَانِي"),
        ("fight against poverty", "مكافحة الفقر"),
        ("health", "صِحَّة"),
        ("education", "تَعْلِيم"),
        ("environment", "بِيئَة"),
        ("social case", "قضية اجتماعية")
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(
        max_length=100,
        choices=ASSOCIATION_CATEGORY_CHOICES
    )
    email = models.EmailField(unique=True)
    photo = models.ImageField(
        upload_to="Profile_pictures/Association/",
        default="Profile_pictures/default.jpg",
        null=True,
        blank=True
    )
    receipt = models.ImageField(
        upload_to="Receipt",
        default=None,
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.nom} - {self.category}"
