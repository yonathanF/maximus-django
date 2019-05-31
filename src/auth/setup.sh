cd /app/authService
python manage.py migrate 
python manage.py flush --noinput 
mod_wsgi-express start-server --working-directory /app/authService --reload-on-changes /app/authService/authService/wsgi.py
