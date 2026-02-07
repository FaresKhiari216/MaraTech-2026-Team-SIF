from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = [
            'category',
            'title',
            'photo',
            'description',
            'emergency',
            'beneficiary',
            'link'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’annonce'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'emergency': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'beneficiary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bénéficiaire'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Lien cha9a9a.tn'}),
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