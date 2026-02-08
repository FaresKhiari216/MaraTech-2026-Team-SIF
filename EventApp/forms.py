from django import forms
from .models import Event
from UserApp.models import Association

class EventForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_at = cleaned_data.get("start_at")
        finish_at = cleaned_data.get("finish_at")

        # Règle: la date de début doit être antérieure ou égale à la date de fin
        if start_at and finish_at and start_at > finish_at:
            self.add_error(
                "finish_at",
                "La date de fin doit être postérieure ou égale à la date de début.",
            )

        return cleaned_data

    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'n_participants',
            'start_at',
            'finish_at',
            'status',
            'image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l’évènement'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'n_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'start_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'finish_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'title': {
                'required': "Le titre de l'évènement est obligatoire.",
                'max_length': "Le titre est trop long.",
            },
            'description': {
                'required': "La description est obligatoire.",
            },
            'n_participants': {
                'required': "Le nombre de participants est obligatoire.",
                'invalid': "Veuillez saisir un nombre valide.",
            },
            'start_at': {
                'required': "La date de début est obligatoire.",
                'invalid': "Veuillez saisir une date valide.",
            },
            'finish_at': {
                'required': "La date de fin est obligatoire.",
                'invalid': "Veuillez saisir une date valide.",
            },
            'status': {
                'required': "Le statut est obligatoire.",
            },
        }

class EventSearchForm(forms.Form):
    keywords = forms.CharField(
        label="Mots-clés",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre ou description...'})
    )

    association = forms.ModelChoiceField(
        label="Association",
        queryset=Association.objects.all().order_by("name"),
        required=False,
        empty_label="Toutes les associations",
        widget=forms.Select(attrs={'class': 'form-control'})
    )