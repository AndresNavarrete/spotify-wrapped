-- Insert new artists and update old records
INSERT INTO
   public.artists 
   SELECT
      * 
   FROM
      public.workspace_artists
      ON conflict (id) DO 
      UPDATE
      SET
         spotify_url = EXCLUDED.spotify_url,
         image_url = EXCLUDED.image_url;
