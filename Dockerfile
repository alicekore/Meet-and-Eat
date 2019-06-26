FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV DECOUPLE_CONFIGURATION="production"
RUN mkdir /config
ADD config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /scripts
ADD scripts /scripts
WORKDIR /meeteat
CMD ["/scripts/wait-for-it.sh" , "db:5432" , "--strict" , "--timeout=300" , "--" , "/scripts/start.sh"]
