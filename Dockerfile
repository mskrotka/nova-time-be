FROM python:3.12-slim

RUN mkdir /app
RUN mkdir /app/logs
RUN mkdir /app/letsencrypt

COPY app/ /app/

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install pipenv

COPY Pipfile /app/
COPY Pipfile.lock /app/
WORKDIR /app/

RUN pipenv lock --clear --verbose
RUN pipenv install --system --deploy --ignore-pipfile

# Utworzenie katalogu na logi
RUN mkdir -p /app/logs && chmod 777 /app/logs

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
