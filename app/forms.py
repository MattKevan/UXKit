from django import forms
from .models import Persona, Project

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['name', 'gender', 'age', 'bio', 'needs', 'frustrations', 'goals']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'needs': forms.Textarea(attrs={'rows': 3}),
            'frustrations': forms.Textarea(attrs={'rows': 3}),
            'goals': forms.Textarea(attrs={'rows': 3}),
            'gender': forms.Select(choices=Persona.GENDER_CHOICES),
        }

class CreateProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']