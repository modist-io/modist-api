FROM postgres:latest

COPY docker/db/initdb.d /docker-entrypoint-initdb.d/
