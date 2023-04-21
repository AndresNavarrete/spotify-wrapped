
# Documentation
## Database setup


I have followed [this tutorial](https://devopscube.com/install-postgresql-on-ubuntu/) to set up Postgres database on a Ubuntu server. To connect with it we must configure the following enviroment variables. I recommend to have a different enviroment for production and develop. 

```sh
PG_USER=""
PG_PASS=""
PG_DB=""

PG_HOST_DEV=""
PG_PORT_DEV=""

PG_HOST_PROD=""
PG_PORT_PROD=""
```

## Spotify API setup
 
To use Spotify API we must configure an authorizion token. For the purpose of this project the most suitable one is the [authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow). Follow those steps have acces to your personal Spotify Account data. 

Ultimately, you will need these enviroment variables to make it work.

```sh
CLIENT_ID=""
CLIENT_SECRET=""
REFRESH_TOKEN=""
```

## Airflow setup

Basically follow [this quickstart guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html) to install Airflow locally. In addition, install the [Postgres Airflow plugin](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html#installation). Then, add the folowing variables .

* `ROOT_PATH`: The ablosulte root path og the project 
* `PIPENV_PATH` the python envitoment location. `pipenv --venv` is recommended to find the correct path.

Also, add the `postgres_spotify_app` connection to the connection using the same data from the Database setup section.

## Simple Crontab Setup

If you need a simpler version of the ETL without using Airflow you can set a cronjob using the following command 

```sh
crontab -l | { cat; echo "0 0 * * * bash bash/spotify_daily_etl.sh"; } | crontab -
```


