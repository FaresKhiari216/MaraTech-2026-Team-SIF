from django.db import models
from UserApp.models import User, Association

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ("handicap", "Handicap"),
        ("maladies", "Maladies"),
        ("enfants", "Enfants"),
        ("education", "Education"),
        ("renovation", "Renovation"),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="handicap"
    )
    association = models.ForeignKey(
        Association,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
        help_text="Association ayant créé cette annonce",
    )
    title = models.CharField(max_length=100, blank=False, null=False)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, help_text="Montant plafond à atteindre")
    target_amount_achieved = models.BooleanField(default=False, help_text="Indique si le montant cible a été atteint")
    views = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to="Announcements/", blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    emergency = models.BooleanField(default=False)
    beneficiary = models.CharField(max_length=100, blank=False, null=False)
    link = models.URLField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Donation(models.Model):
    donateur = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="dons"
    )
    announcement = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        related_name="dons"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Don de {self.donateur} pour {self.announcement}"
