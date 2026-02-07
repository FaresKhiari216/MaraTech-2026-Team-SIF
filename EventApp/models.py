from django.db import models
from UserApp.models import Association

STATUS_CHOICES = [
        ("upcoming", "مُقْبِل"),
        ("finished", "اِنْتَهَى"),
        ("cancelled", "ألغت"),
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
        default="À venir"
    )

    image = models.ImageField(
        upload_to="Events/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title
