# stocks-data

download all csvs and put them in a folder called `data`

run `docker-compose up`

This will start the mysql docker container, and run python preprocessing scipts on the csvs

get into the container using `docker exec -it project_db_1 bash`

inside the container, run the following to create the database

```
cd var/lib/mysql-files
mysql -uroot -proot
source CreateStocksDatabase.sql
```