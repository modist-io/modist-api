FROM python:3.7
WORKDIR /app

# add migrations
COPY alembic/ ./alembic
COPY alembic.ini ./alembic.ini

# add source code
COPY src/ ./src/

# add dependency management configuration
COPY Pipfile* ./
COPY setup.* ./

RUN pip install pipenv uvicorn
RUN pipenv install --system

COPY docker/app/entrypoint.sh ./entrypoint.sh

EXPOSE 80
ENTRYPOINT [ "./entrypoint.sh" ]
