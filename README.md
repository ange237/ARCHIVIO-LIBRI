# ARCHIVIO-LIBRI
AGM Archive è un'applicazione per la gestione digitale di un archivio di libri, pensata per biblioteche e istituti scolastici.

## Requisiti

- Python 3.10+
- Django 5.2+
- SQLite
- Bootstrap 5 (incluso nei template)
- html
- css

## Installazione
1. Clona il progetto:
  git clone https://github.com/ange237/ARCHIVIO-LIBRI.git
2. Crea un ambiente virtuale:
  python -m venv env
3. Installa le dipendenze (django in questo caso):
  pip install django
4. Esegui le migrazioni:
  1- python manage.py makemigrations 
  2- python manage.py migrate
5. Avvia il server : python manage.py runserver

## Utilizzo

- Vai su `http://127.0.0.1:8000`
- Aggiungi un libro tramite "Aggiungi Libro"
- Ricerca un libro nella sezione "Ricerca"
- Visualizza dettagli, modifica o elimina un libro

## Struttura del Progetto
gestione_archivio/
├── libro/ # App per la gestione dei libri
│ ├── models.py # Modelli dei dati
│ ├── views.py # Logica delle viste
│ ├── templates/ # Template HTML
├── static/ # immagini del progetto
├── media/ # copertine libri
├── manage.py

