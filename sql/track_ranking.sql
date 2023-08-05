-- Clear current ranking
TRUNCATE TABLE public.tracks_ranking ;
-- Fill current ranking
INSERT INTO
   public.tracks_ranking 
   SELECT
      id AS track_id,
      ROW_NUMBER() OVER () AS ranking 
   FROM
      public.workspace_tracks t;
-- Add historic records
DELETE FROM
   public.tracks_ranking_history 
WHERE
   date = CURRENT_DATE;

INSERT INTO
   public.tracks_ranking_history 
   SELECT
      CURRENT_DATE,
      tr.ranking,
      tr.track_id 
   FROM
      public.tracks_ranking tr ;
