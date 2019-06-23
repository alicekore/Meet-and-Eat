FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /media/meetandeat
RUN mkdir /static
ADD meeteat/meetandeat/static /static/
RUN mkdir /meeteat
ADD meeteat /meeteat
RUN mkdir /scripts
ADD scripts /scripts
WORKDIR /meeteat
CMD ["/scripts/wait-for-it.sh" , "db:5432" , "--strict" , "--timeout=300" , "--" , "/scripts/start.sh"]
