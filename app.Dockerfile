FROM python:3.7
WORKDIR /app

COPY . .

RUN pip install pipenv
RUN pipenv install --system

COPY docker/app/entrypoint.sh ./entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
