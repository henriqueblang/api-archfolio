FROM postgis/postgis
COPY src/sql/schema.sql /docker-entrypoint-initdb.d/
