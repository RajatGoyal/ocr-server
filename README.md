Django server, exposes a api endpoint to submit request for OCR, Runs OCR and gives the result back in response.

Development Requirements
====
* Python
* Django==1.6.5
* Pillow==2.5.1
* django-tastypie==0.11.1
* pytesseract==0.1
* python-dateutil==2.2
* python-mimeparse==0.1.4
* six==1.7.3
* wsgiref==0.1.2
* Tesseract 3.02
* Tastypie

Deployment Requirements
====
* Python
* Django==1.6.5
* Pillow==2.5.1
* django-tastypie==0.11.1
* pytesseract==0.1
* python-dateutil==2.2
* python-mimeparse==0.1.4
* six==1.7.3
* wsgiref==0.1.2
* Tesseract 3.02
* Tastypie
* Gunicorn
* Nginx
* Supervisor

Gunicorn, Nginx and Supervisor deployment files can be found in '/bin'
