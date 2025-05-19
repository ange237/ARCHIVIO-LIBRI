"""
URL configuration for gestione_archivio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libro.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name='home'), # per la home page
    path('lista_libri/', lista_libri_disponibili, name='lista_libri'), #per mostrare la lista dei libri disponibili nel nostro archivio
    path('aggiungi_libro/', aggiungi_libro, name='aggiungi_libro'),# per aggiungere un libro nel nostro archivio
    path('modifica/<int:libro_id>/', modifica_libro, name='modifica_libro'),#per modificare un libro nel nostro archivio
    path('elimina/<int:libro_id>/', cancella_libro, name='elimina_libro'),#per eliminare un libro nel nostro archivio
    path('ricerca_libro/', ricerca_libro, name='ricerca_libro'), # per ricercare un libro nell'archivio
    path('libro/<int:id>//',dettagli_libro, name='dettagli_libro'), # per i dettagli di un libro
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    