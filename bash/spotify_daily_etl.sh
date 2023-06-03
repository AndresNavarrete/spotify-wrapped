#!/bin/bash
export $(grep -v '^#' .env | xargs)
cd $ROOT_PATH &&  python3 commands/run_cleaning_query.py 
cd $ROOT_PATH/bash 
bash save_top_artists.sh 
bash save_top_tracks.sh 
bash sql_transformations.sh
