FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /meeteat;
RUN mkdir /media/meetandeat
WORKDIR /meeteat
CMD python manage.py collectstatic --no-input;python manage.py makemigrations;python manage.py migrate;DECOUPLE_CONFIGURATION=production gunicorn meeteat.wsgi -b 0.0.0.0:8000
