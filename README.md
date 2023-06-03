# Spotify wrapped

[![GitHub Super-Linter](https://github.com/AndresNavarrete/spotify-wrapped/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)

The goal of this repository is to show my personal Spotify Wrapped and some trends on my most listened artists.

Data is fetched from [Spotify API](https://developer.spotify.com/) and stored in a [Postgres](https://www.postgresql.org/) database on a daily basis. This process is orquestrated using [Apache Airflow](https://airflow.apache.org/) and runs on [Docker containers](https://www.docker.com/). 

<img src="/img/project_diagram.png" alt="Project diagram" width="100%"/>

## Recent artist trends
<img src="/img/artist_ranking_trend.png" alt="Artists" width="100%"/>

# Documentation
## Table of Contents <!-- omit in toc -->

- [Database Set up](#database-setup)
- [Spotify API set up](#spotify-api-setup)
- [ETL set up](#etl-setup)
  - [Airflow: Run locally](#airflow-setup-run-locally)
  - [Airflow: Run on container](#airflow-setup-run-on-container-recommended)
  - [Simple Crontab](#simple-crontab-setup)
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


## ETL setup

The data pipeline is modelated as a Extract-Transform-Load process. The recommendation is to use Airflow as the orquestator, but a simple cronjob would to the trick if Airflow is too much for your server.

### Airflow setup: Run locally
Basically follow [this quickstart guide](https://airflow.apache.org/docs/apache-airflow/stable/start.html) to install Airflow locally. In addition, install the [Postgres Airflow plugin](https://airflow.apache.org/docs/apache-airflow-providers-postgres/stable/index.html#installation). 

### Airflow setup: Run on container (recommended)

Build the image with `docker-compose build` and run the cointainer with `docker-compose up`. For more detailed instruction you can read [Running Airflow in Docker
](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker)


Regardless of the installation chosen, add the folowing variables .

* `ROOT_PATH`: The absolute root path of the project 

Also, add the `postgres_spotify_app` connection to the connection using the same data from the Database setup section.

### Simple Crontab Setup

If you need a simpler version of the ETL without using Airflow you can set a cronjob using the following command 

```sh
crontab -l | { cat; echo "0 0 * * * cd <Repository absolute parh> && bash bash/spotify_daily_etl.sh"; } | crontab -
```