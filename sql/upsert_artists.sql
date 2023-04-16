-- Insert new artists and update old records
INSERT INTO
   dev.artists 
   SELECT
      * 
   FROM
      workspace.artists
      ON conflict (id) DO 
      UPDATE
      SET
         spotify_url = EXCLUDED.spotify_url,
         image_url = EXCLUDED.image_url;
