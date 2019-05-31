FROM grahamdumpleton/mod-wsgi-docker:python-3.5
RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ENV LANG=en_US.UTF-8 PYTHONHASHSEED=random \
    PATH=/usr/local/python/bin:/usr/local/apache/bin:$PATH \
    MOD_WSGI_USER=www-data MOD_WSGI_GROUP=www-data
