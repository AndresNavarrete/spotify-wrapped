#!/bin/bash
export PYTHONPATH=$ROOT_PATH
cd $ROOT_PATH &&  $PIPENV_PATH commands/run_cleaning_query.py && echo 'Done run_cleaning_query'
cd $ROOT_PATH/bash 
bash save_top_artists.sh && echo 'Done save_top_artists'
bash save_top_tracks.sh && echo 'Done save_top_tracks'
bash sql_transformations.sh&& echo 'Done sql_transformations'

