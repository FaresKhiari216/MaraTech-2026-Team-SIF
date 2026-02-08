from django.db import models
from django.conf import settings
from UserApp.models import Association

STATUS_CHOICES = [
        ("upcoming", "Bientôt"),
        ("finished", "Terminé"),
        ("cancelled", "Annulé"),
]

class Event(models.Model):
    association = models.ForeignKey(
        Association,
        on_delete=models.CASCADE,
        null=False,
        related_name="association_event",
        default=1
    )
    title = models.CharField(max_length=60, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    n_participants = models.PositiveIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    start_at = models.DateField(blank=False, null=False)
    finish_at = models.DateField(blank=False, null=False)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Bientôt"
    )

    image = models.ImageField(
        upload_to="Events/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title


class EventFollow(models.Model):
    """Lien entre un utilisateur "normal" (non association) et un évènement suivi."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_events",
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="followers",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user} suit {self.event}"
