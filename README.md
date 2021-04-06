# stocks-data

download all csvs and put them in a folder called `data`

run `python3 filter_ipo_csv.py` and `python3 process_financial_data.py`

run `docker-compose up`

get into the container using `docker exec -it project_db_1 bash`

inside the container, run the following to create the database

```
cd var/lib/mysql-files
mysql -uroot -proot
source CreateStocksDatabase.sql
```