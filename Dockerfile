FROM python:3
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    vim

ENV PYTHONUNBUFFERED=1

WORKDIR /code/
ADD . /code

RUN pip install -r requirements.txt


# Server
#RUN python manage.py collectstatic --settings=base.settings.dev

EXPOSE 80 8001 8000
#STOPSIGNAL SIGINT
#CMD ["gunicorn", "base.wsgi:application", "--bind", "0.0.0.0:8000"]