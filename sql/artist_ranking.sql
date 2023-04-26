-- Clear current ranking
TRUNCATE TABLE dev.artists_ranking ;
-- Fill current ranking
INSERT INTO
   dev.artists_ranking 
   SELECT
      id AS artist_id,
      ROW_NUMBER() OVER () AS ranking 
   FROM
      workspace.artists t;
-- Add historic records
DELETE FROM
   dev.artists_ranking_history 
WHERE
   date = CURRENT_DATE;

INSERT INTO
   dev.artists_ranking_history 
   SELECT
      CURRENT_DATE,
      tr.ranking,
      tr.artist_id 
   FROM
      dev.artists_ranking tr ;
