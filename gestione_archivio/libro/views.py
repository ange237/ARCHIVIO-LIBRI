from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from .forms import *
from django.contrib import messages #per i messaggi
from django.core.paginator import Paginator
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import Counter
import io
import base64 



def home(request):
   return render(request,'libro/home.html')


#funzione per vedere la lista dei libri disponibili
"""def lista_libri_disponibili(request):
    libri = Libro.objects.all()  # Ottieni tutti i libri dal database
    return render(request, 'libro/lista_libri.html', {'libri': libri})"""

#versione con la paginazione
def lista_libri_disponibili(request):
    libri_list = Libro.objects.all() 
    paginator = Paginator(libri_list, 12)  # 12 libri per pagina

    page_number = request.GET.get('page')  # es: /libri/?page=2
    page_obj = paginator.get_page(page_number)

    return render(request, 'libro/lista_libri.html', {'page_obj': page_obj})

def dettagli_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    return render(request, 'libro/dettagli_libro.html', {'libro': libro})


#funzione per aggiungere un libro
"""def aggiungi_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Salva il libro
            return redirect('lista_libri')  # Redirect alla lista dei libri
    else:
        form = LibroForm()
    return render(request, 'libro/aggiungi_libro.html', {'form': form})"""

#versione con messagio di errore
def aggiungi_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Il libro è stato aggiunto con successo!")
            return redirect('lista_libri')  # torna a lista libri
        else:
            messages.error(request, "C'è stato un errore nell'aggiungere il libro.") # manda un messagio di errore.
    else:
        form = LibroForm()

    return render(request, 'libro/aggiungi_libro.html', {'form': form})




#funzione per modificare un libro
"""def modifica_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('lista_libri')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libro/modifica_libro.html', {'form': form, 'libro': libro})"""

def modifica_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        
        if form.is_valid():
            form.save()
            # Aggiungere un messaggio di successo
            messages.success(request, f"Il libro '{libro.titolo}' è stato modificato con successo!")
            return redirect('lista_libri')  # torna alla lista dei libri
    else:
        form = LibroForm(instance=libro)
    
    return render(request, 'libro/modifica_libro.html', {'form': form, 'libro': libro})


#funzione per cancellare un libro dall'archivio
"""def cancella_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()  # Elimina il libro dal database
        return redirect('lista_libri')
    return render(request, 'libro/elimina_libro.html', {'libro': libro})"""


def cancella_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        libro.delete()  # Elimina il libro dal database
        # Aggiungi un messaggio di successo
        messages.success(request, f"Il libro '{libro.titolo}' è stato cancellato con successo!")
        return redirect('lista_libri')  # Redirigi alla lista dei libri
    
    return render(request, 'libro/elimina_libro.html', {'libro': libro})

"""def cancella_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        libro.delete()  # Elimina il libro dal database
        return redirect('lista_libri')  # Redirect alla lista dei libri con un messaggio di successo

    return render(request, 'libro/elimina_libro.html', {'libro': libro})"""

#funzione per ricercare un libro nell'archivio
def ricerca_libro(request):

    form = RicercaLibroForm(request.GET)  # Otteniamo i dati della richiesta GET
    libri_trovati = Libro.objects.all()  # Iniziamo prendendo tutti i libri

    if form.is_valid():
        # Questi sono i filtri per ogni campo del form
        if form.cleaned_data['titolo']: # se il campo c'è.
            libri_trovati = libri_trovati.filter(titolo__icontains=form.cleaned_data['titolo'])
        
        if form.cleaned_data['autore']: 
            libri_trovati = libri_trovati.filter(autore__icontains=form.cleaned_data['autore'])
        
        if form.cleaned_data['anno_pubblicazione']:
            libri_trovati = libri_trovati.filter(anno_pubblicazione=form.cleaned_data['anno_pubblicazione'])
        
        if form.cleaned_data['categoria']:
            libri_trovati = libri_trovati.filter(categoria=form.cleaned_data['categoria'])

    return render(request, 'libro/ricerca_libro.html', {'form': form,'libri': libri_trovati})

#funzione pe l'analisi dati : per trovare la categoria con piu libri presenti
def diag_libri_categoria(request):
    libri = Libro.objects.all() # ottengo tutti i libri della mai base di dati
    #categorie = ['romanzo','fantascienza','bd','horor','altro'] non funziona cosi perchè conta solo 1 per ogni categoria
    categorie = [libro.get_categoria() for libro in libri]#avremmo una lista di tutte le categorie per ogni libro con il nome che si puo ripetere
    #esempio: [romanzo,romanzo,bd,fantascienza,...]
    conteggio = Counter(categorie)
    #myset = pd.DataFrame(libri) non mi serve.
    categorie_list = list(conteggio.keys())
    conteggio_list = list(conteggio.values())
    plt.bar(categorie_list, conteggio_list)
    plt.xlabel('Categorie libri')
    plt.ylabel('Numero di libri')
    plt.title("Numero di libri per categoria")

    # 2. Salva il grafico in un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight') # bbox_inches='tight' per evitare il taglio
    buffer.seek(0)

    # 3. Convertilo in base64
    image_png = buffer.getvalue()
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close()

    # 4. Passa la stringa al template
    return render(request, 'libro/libri_per_categoria.html', {'grafico': grafico_base64})

##funzione pe l'analisi dati : per trovare l'autore con piu libri presenti nell'archivio
def diag_libri_autore(request):
    libri = Libro.objects.all() # ottengo tutti i libri della mai base di dati
    autori = [libro.get_autore() for libro in libri]
    conteggio = Counter(autori)
    autore_list = list(conteggio.keys())
    conteggio_list = list(conteggio.values())
    plt.figure(figsize=(10, 4))  # Aumenta la dimensione del grafico
    plt.bar(autore_list, conteggio_list)
    plt.xlabel('Autore')
    plt.ylabel('Numero di libri')
    plt.title("Numero di libri per autore")
    plt.xticks(rotation=45, ha='right')
    # 2. Salva il grafico in un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')  # bbox_inches='tight' per evitare il taglio
    buffer.seek(0)
    # 3. Convertilo in base64
    image_png = buffer.getvalue()
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close()
    # 4. Passa la stringa al template
    return render(request, 'libro/libri_per_autori.html', {'grafico': grafico_base64})

##funzione pe l'analisi dati : per trovare l'anno di publicazione con più libri
def diag_libri_anno(request):
    libri = Libro.objects.all() # ottengo tutti i libri della mai base di dati
    anni = [libro.get_anno_pubblicazione() for libro in libri]
    conteggio = Counter(anni)
    anno_list = list(conteggio.keys())
    conteggio_list = list(conteggio.values())
    plt.figure(figsize=(10, 6))  # Aumenta la dimensione del grafico
    plt.bar(anno_list, conteggio_list)
    plt.xlabel('anno di publicazione')
    plt.ylabel('Numero di libri')
    plt.title("Numero di libri per anno di publicazione")
    plt.xticks(rotation=45, ha='right')
    # 2. Salva il grafico in un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')  # bbox_inches='tight' per evitare il taglio
    buffer.seek(0)
    # 3. Convertilo in base64
    image_png = buffer.getvalue()
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close()
    # 4. Passa la stringa al template
    return render(request, 'libro/libri_per_anno.html', {'grafico': grafico_base64})


##funzione pe l'analisi dati : per trovare l'editore  con più libri
def diag_libri_editore(request):
    libri = Libro.objects.all() # ottengo tutti i libri della mai base di dati
    editori = [libro.get_editore() for libro in libri]
    conteggio = Counter(editori)
    editore_list = list(conteggio.keys())
    conteggio_list = list(conteggio.values())
    plt.bar(editore_list, conteggio_list)
    plt.xlabel('editore')
    plt.ylabel('Numero di libri')
    plt.title("Numero di libri per editore")
    plt.xticks(rotation=45, ha='right')
    # 2. Salva il grafico in un buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png',bbox_inches='tight')  # bbox_inches='tight' per evitare il taglio
    buffer.seek(0)
    # 3. Convertilo in base64
    image_png = buffer.getvalue()
    grafico_base64 = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    plt.close()
    # 4. Passa la stringa al template
    return render(request, 'libro/libri_per_editori.html', {'grafico': grafico_base64})

#view per veder le statistiche
def statistici(request):
     return render(request,'libro/statistici.html')

