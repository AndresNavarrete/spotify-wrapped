import os

from src.clients import Postgres


class Queries_Manager:
    def __init__(self):
        self.postgres = Postgres()
        self.template_searchpath = os.getenv("ROOT_PATH") + "/sql"
        self.cleaning_task = "clean_workspace"
        self.sql_tasks = [
            "upsert_artists",
            "upsert_tracks",
            "track_ranking",
            "artist_ranking",
        ]

    def execute_all_tasks(self):
        for task in self.sql_tasks:
            self.execute_task(task)
        self.execute_cleaning_task()

    def execute_task(self, task_name):
        query = self.get_sql_script(task_name)
        self.postgres.execute_raw_query(query)

    def get_sql_script(self, script_name):
        file_path = f"{self.template_searchpath}/{script_name}.sql"
        return open(file_path, "r").read()

    def execute_cleaning_task(self):
        self.execute_task(self.cleaning_task)
