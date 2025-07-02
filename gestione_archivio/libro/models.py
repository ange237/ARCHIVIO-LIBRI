from django.db import models
import random
from django.core.validators import *



# Funzione per generare il codice univoco del libro secondo il formato:
#LIB+numero 25 moliplicato per un numero tra 0 e 1000
def genera_codice_univoco():
    # Prefisso fisso per il libro
    prefisso = "LIB"
    num =25
    n = random.randint(0,1000) *25
    return prefisso + str(n)
    
    
    


#libri del mio archivio
class Libro(models.Model):
    #categorie di romanzo
    R =  'ROMANZO'
    FS = 'FANTASCIENZA'
    BD = 'BD'
    HO = 'HOROR'
    AL = 'ALTRO'

    CATEGORY_CHOICES = [
        (R, 'romanzo'),
        (FS, 'fantascienza'),
        (BD, 'bd'),
        (HO, 'horor'),
        (AL, 'altro'),
    ]


    titolo = models.CharField(max_length=200)
    autore = models.CharField(max_length=100)
    anno_pubblicazione = models.IntegerField(null=True,blank=True,                                
        validators=[
            MinValueValidator(1000),      # Il valore deve essere >= 1000
            MaxValueValidator(2025),     # Il valore deve essere <= 2025
        ])
    immagine = models.ImageField(upload_to='copertine_libri/', null=True, blank=True)  # Il campo immagine
    codice_univoco = models.CharField(max_length=50, unique=True, default=genera_codice_univoco, editable=False)
    editore = models.CharField(max_length=100)
    categoria = models.CharField(
        max_length=12,
        choices=CATEGORY_CHOICES,
        default=AL,
        null=True,
        blank=True
    )
    descrizione = models.TextField(blank=True, null=True)

    """experience = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),      # Il valore deve essere >= 0
            MaxValueValidator(100),     # Il valore deve essere <= 100
        ]
    )"""

    def get_titolo(self):
        return self.titolo
    
    # Getter e Setter per l'autore
    def get_autore(self):
        return self.autore

    # Getter per l'anno di pubblicazione
    def get_anno_pubblicazione(self):
        return self.anno_pubblicazione

    # Getter per l'immagine
    def get_immagine(self):
        return self.immagine

    # Getter per il codice univoco
    def get_codice_univoco(self):
        return self.codice_univoco

    # Getter  per l'editore
    def get_editore(self):
        return self.editore

    # Getter per la categoria
    def get_categoria(self):
        return self.categoria

    def __str__(self):
        return f"{self.titolo} {self.autore} {self.anno_pubblicazione} {self.codice_univoco} {self.editore} {self.categoria}"
    

