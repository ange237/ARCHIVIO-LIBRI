from django.shortcuts import render, redirect, get_object_or_404
from .models import Libro
from .forms import *
from django.contrib import messages #per i messaggi
from django.core.paginator import Paginator


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

