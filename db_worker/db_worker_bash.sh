#!/usr/local/bin/bash

apk add --no-cache postgresql-client

pg_dump --host=db --port=5432 --username=northwind_user --no-password --dbname=northwind --data-only --file=/data/teste.sql

#echo 'carlos' > /data/teste.csv
