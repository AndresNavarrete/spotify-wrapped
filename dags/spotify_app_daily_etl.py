from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

ROOT_PATH = Variable.get("ROOT_PATH")
PIPENV_PATH = Variable.get("PIPENV_PATH")

with DAG(
    dag_id="spotify_app_daily_etl",
    start_date=datetime(2023, 3, 18),
    schedule_interval="0 6 * * *",
    catchup=False,
    owner="Andres_Navarrete",
    template_searchpath=[ROOT_PATH],
) as dag:
    save_top_tracks = BashOperator(
        task_id="save_top_tracks",
        bash_command=f"cd $ROOT_PATH && $ROOT_PATH/python3 src/get_items.py tracks ",
    )
    save_top_artists = BashOperator(
        task_id="save_top_artists",
        bash_command=f"cd $ROOT_PATH && $ROOT_PATH/python3 src/get_items.py artists ",
    )
    upsert_tracks = PostgresOperator(
        task_id="upsert_tracks",
        postgres_conn_id="postgres_spotify_app",
        sql="sql/upsert_tracks.sql",
    )
    upsert_artists = PostgresOperator(
        task_id="upsert_artists",
        postgres_conn_id="postgres_spotify_app",
        sql="sql/upsert_artists.sql",
    )
    track_ranking = PostgresOperator(
        task_id="track_ranking",
        postgres_conn_id="postgres_spotify_app",
        sql="sql/track_ranking.sql",
    )
    clean_workspace = PostgresOperator(
        task_id="clean_workspace",
        postgres_conn_id="postgres_spotify_app",
        sql="sql/clean_workspace.sql",
    )
    (
        [save_top_tracks, save_top_artists]
        >> [upsert_tracks, upsert_artists]
        >> track_ranking
        >> clean_workspace
    )
