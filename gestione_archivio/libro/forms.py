from django import forms
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titolo', 'autore', 'anno_pubblicazione', 'immagine', 'editore', 'categoria','descrizione']


class RicercaLibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titolo', 'autore', 'anno_pubblicazione', 'categoria']  # solo i campi che vuoi nel form
        widgets = {
            'titolo': forms.TextInput(attrs={'placeholder': 'Inserisci il titolo'}),
            'autore': forms.TextInput(attrs={'placeholder': 'Inserisci l\'autore'}), 
            'anno_pubblicazione': forms.NumberInput(attrs={'placeholder': 'Inserisci l\'anno di pubblicazione'}),
            'categoria': forms.Select(attrs={'placeholder': 'Seleziona la categoria'}),
        }

    # Impostiamo i campi come non obbligatori
    def __init__(self, *args, **kwargs):
        super(RicercaLibroForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False        