from django import forms
from .models import Event
from UserApp.models import Association

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