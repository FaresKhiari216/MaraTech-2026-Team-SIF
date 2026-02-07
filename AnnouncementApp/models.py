from django.db import models
from UserApp.models import User

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ("handicap", "إعاقة"),
        ("maladies", "أمراض"),
        ("enfants", "أطفال"),
        ("education", "تعليم"),
        ("renovation", "ترميم"),
        ("autres", "أخرى"),
    ]

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="autres"
    )
    title = models.CharField(max_length=100, blank=False, null=False)
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
