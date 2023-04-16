
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
