-- Clear current ranking
TRUNCATE TABLE dev.tracks_ranking ;
-- Fill current ranking
INSERT INTO
   dev.tracks_ranking 
   SELECT
      id AS track_id,
      ROW_NUMBER() OVER () AS ranking 
   FROM
      workspace.tracks t;
-- Add historic records
DELETE FROM
   dev.tracks_ranking_history 
WHERE
   date = CURRENT_DATE;

INSERT INTO
   dev.tracks_ranking_history 
   SELECT
      CURRENT_DATE,
      tr.ranking,
      tr.track_id 
   FROM
      dev.tracks_ranking tr ;
