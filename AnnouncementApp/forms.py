from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'category',
            'title',
            'photo',
            'target_amount',
            'description',
            'emergency',
            'beneficiary',
            'link',
            'target_amount_achieved',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’annonce'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant plafond à atteindre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'beneficiary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bénéficiaire'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien cha9a9a.tn'}),
            'target_amount_achieved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
            'category': {
                'required': "La catégorie est obligatoire.",
            },
            'title': {
                'required': "Le titre de l'annonce est obligatoire.",
                'max_length': "Le titre est trop long.",
            },
            'target_amount': {
                'required': "Le montant cible est obligatoire.",
                'invalid': "Veuillez saisir un montant valide.",
            },
            'description': {
                'required': "La description est obligatoire.",
            },
            'beneficiary': {
                'required': "Le nom du bénéficiaire est obligatoire.",
            },
            'link': {
                'required': "Le lien de vérification est obligatoire.",
                'invalid': "Veuillez saisir une URL valide.",
            },
        }

class AnnouncementSearchForm(forms.Form):
    category = forms.ChoiceField(
        choices=[("", "Tous")] + Announcement.CATEGORY_CHOICES,
        label="Catégorie",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    keywords = forms.CharField(
        label="Mots-clés",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre ou description...'})
    )
    emergency = forms.BooleanField(
        label="Cas urgent",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )