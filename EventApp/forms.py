from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'n_participants',
            'start_at',
            'finish_at',
            'status',
            'image'
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

class EventSearchForm(forms.Form):
    query = forms.CharField(
        label="Rechercher un évènement",
        max_length=60,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom de l’évènement...'
        })
    )
