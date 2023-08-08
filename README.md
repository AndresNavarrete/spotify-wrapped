# Spotify wrapped

The goal of this repository is to show my personal Spotify data with some trends on my most listened artists and songs.

Data is fetched from [Spotify API](https://developer.spotify.com/) and stored in a [Postgres](https://www.postgresql.org/) database on a daily basis. The stored data is my daily short-term ranking of most listened song and artists. This process is orquestrated using [Apache Airflow](https://airflow.apache.org/) and runs on [Docker containers](https://www.docker.com/) and the data is accesible using a [Django API REST](https://www.djangoproject.com/)

<img src="/img/project_diagram.png" alt="Project diagram" width="100%"/>

## Top artists
<img src="/img/ranking_artists.png" alt="Artists" width="100%"/>

## Top songs
<img src="/img/ranking_songs.png" alt="Songs" width="100%"/>

# Documentation
## Table of Contents <!-- omit in toc -->

- [Database & API setup](#database-setup)
- [Spotify API setup](#spotify-api-setup)
- [ETL setup](#etl-setup)
  - [Airflow: Run locally](#airflow-setup-run-locally)
  - [Airflow: Run on container](#airflow-setup-run-on-container-recommended)
  - [Simple Crontab](#simple-crontab-setup)
## Database & Django setup
The Postgres database runs on docker container. It holds some Django related tables, the historic data of artists, songs and the most recent ranking data. 


A [Django API](https://www.djangoproject.com/) is also provided in a docker container to fetch data from the database and expose it. Currently the API supports the historic trend of most listened artists and songs.


To build the images and run the container just run
```sh
bash bash/docker_init.sh
```
This command will take take of start the database and generate all tables and views needed for this project. Also will initialize the API Rest for fetching data from the database.

For this to work you need the following enviroment variables.

```sh
# Postgres
POSTGRES_DB=""
POSTGRES_PASSWORD=""
POSTGRES_USER=""
POSTGRES_PORT=""
POSTGRES_HOST=""

# Django
DJANGO_ANON_USER=""
DJANGO_ANON_PASSWORD=""
DJANGO_SECRET_KEY=""
DJANGO_PORT=""
```
## Spotify API setup
 
To use Spotify API we must configure an authorizion token. For the purpose of this project the most suitable one is the [authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow). Follow those steps have acces to your personal Spotify Account data. 

Ultimately, you will need these enviroment variables to make it work.

```sh
# Spotify
CLIENT_ID=""
CLIENT_SECRET=""
REFRESH_TOKEN=""
```


## ETL setup

The data pipeline is modelated as a Extract-Transform-Load process. The recommendation is to use Airflow as the orquestator, but a simple cronjob would to the trick if Airflow is too much for your server.

### Airflow setup: Run locally
Basically follow [this quickstart guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html) to install Airflow locally. In addition, install the [Postgres Airflow plugin](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html#installation). 

### Airflow setup: Run on container (recommended)

Build the image with `docker-compose build` in the airflow directory and run the cointainer with `docker-compose up`. For more detailed instruction you can read [Running Airflow in Docker
](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker)


Also, add the `postgres_spotify_app` connection to the connection using the same data from the Database setup section.

### Simple Crontab Setup

If you need a simpler version of the ETL without using Airflow you can set a cronjob using the following command 

```sh
crontab -l | { cat; echo "0 0 * * * (date; cd <Repository absolute path> && bash bash/spotify_daily_etl.sh) >> logs/spotify_logs.log 2>&1 "; } | crontab -
```