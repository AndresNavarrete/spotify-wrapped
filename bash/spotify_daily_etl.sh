#!/bin/bash
export PYTHONPATH=$ROOT_PATH
cd $ROOT_PATH &&  $PIPENV_PATH commands/run_cleaning_query.py 
cd $ROOT_PATH/bash 
bash save_top_artists.sh 
bash save_top_tracks.sh 
bash sql_transformations.sh

