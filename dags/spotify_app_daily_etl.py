from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from src.top_items import get_top_artists, get_top_tracks

root_folder = Variable.get("root_folder")
with DAG(
    dag_id="spotify_app_daily_etl",
    start_date=datetime(2023, 3, 18),
    schedule_interval="0 6 * * *",
    catchup=False,
    owner="Andres_Navarrete",
    template_searchpath=[root_folder],
) as dag:
    save_top_tracks = PythonOperator(
        task_id="get_top_tracks",
        python_callable=get_top_tracks,
    )
    save_top_artists = PythonOperator(
        task_id="get_top_artists",
        python_callable=get_top_artists,
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
