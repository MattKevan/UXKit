from django import forms
from .models import Persona, Project, LeanUXCanvas

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

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'description']
		widgets = {
			'description': forms.Textarea(attrs={'rows': 3}),
		}

class LeanUXCanvasForm(forms.ModelForm):
	class Meta:
		model = LeanUXCanvas
		fields = ['name', 'problem']
		widgets = {
			'problem': forms.Textarea(attrs={'rows': 3}),
		}