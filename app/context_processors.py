from .forms import PersonaForm

def persona_form(request):
    return {'form': PersonaForm()}