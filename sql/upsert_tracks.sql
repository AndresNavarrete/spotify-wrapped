-- Insert new tracks and update old records
INSERT INTO
   public.tracks 
   SELECT
      * 
   FROM
      public.workspace_tracks
      ON conflict (id) DO 
      UPDATE
      SET
         spotify_url = EXCLUDED.spotify_url,
         album_image_url = EXCLUDED.album_image_url;