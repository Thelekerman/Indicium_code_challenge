docker exec -it postgres_2 psql -U northwind_user -d northwind -f ./scripts/drop_constraints.sql

docker exec -it postgres_2 psql -U northwind_user -d northwind -f ./scripts/add_constraints.sql
