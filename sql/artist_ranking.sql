-- Clear current ranking
TRUNCATE TABLE public.artists_ranking ;
-- Fill current ranking
INSERT INTO
   public.artists_ranking 
   SELECT
      id AS artist_id,
      ROW_NUMBER() OVER () AS ranking 
   FROM
      public.workspace_artists t;
-- Add historic records
DELETE FROM
   public.artists_ranking_history 
WHERE
   date = CURRENT_DATE;

INSERT INTO
   public.artists_ranking_history 
   SELECT
      CURRENT_DATE,
      tr.ranking,
      tr.artist_id 
   FROM
      public.artists_ranking tr ;
