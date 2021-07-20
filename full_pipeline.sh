#!/bin/bash
# full_pipeline.sh

if [[ -z $1 ]]; then
  sed -i "s/DATE=.*/DATE=/" .env
  cat .env
else
  sed -i "s/DATE=.*/DATE=${1}/" .env
  cat .env
fi

docker-compose up -d db
if [[ $? -ne 0 ]]; then
  echo 'Broken pipeline when initializing db service'
  break
fi

docker-compose up -d final_db
if [[ $? -ne 0 ]]; then
  echo 'Broken pipeline when initializing final_db service'
  break
fi

echo 'Starting the csv_worker service!'
docker-compose run --rm csv_worker 2>> ./logs/csv_worker.log
if [[ $? -ne 0 ]]; then
  echo 'Broken pipeline when running csv_worker service'
  break
fi

echo 'Waiting for db service to fully initialize...'
sleep 30

counter=0
echo 'Starting the db_worker service!'
until docker-compose run --rm db_worker 2>> ./logs/db_worker.log; do
  >&2 echo 'Trying to rerun the db_worker service'
  ((counter++))
  if [[ $counter -ge 5 ]]; then
    >&2 echo 'Limit of retries exceeded'
    break
  fi
  sleep 10
done

counter=0
echo 'Starting the final_db_worker service!'
until docker-compose run --rm final_db_worker 2>> ./logs/final_db_worker.log; do
  >&2 echo 'Trying to rerun the db_worker service'
  ((counter++))
  if [[ $counter -ge 5 ]]; then
    >&2 echo 'Limit of retries exceeded'
    break
  fi
  sleep 10
done
