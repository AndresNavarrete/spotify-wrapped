
CREATE TABLE public.artists (
	id varchar NOT NULL,
	"name" varchar NULL,
	spotify_url varchar NULL,
	image_url varchar NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT artists_pk PRIMARY KEY (id)
);

CREATE TABLE public.tracks (
	id varchar NOT NULL,
	artist_id varchar NULL,
	album_id varchar NULL,
	"name" varchar NULL,
	artist varchar NULL,
	spotify_url varchar NULL,
	album_image_url varchar NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT tracks_pk PRIMARY KEY (id)
);

CREATE TABLE public.tracks_ranking (
	track_id varchar NOT NULL,
	ranking int8 NOT NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT tracks_ranking_pk PRIMARY KEY (ranking),
	CONSTRAINT tracks_ranking_fk FOREIGN KEY (track_id) REFERENCES public.tracks(id)
);

CREATE TABLE public.tracks_ranking_history (
	"date" date NOT NULL,
	ranking int8 NOT NULL,
	track_id varchar NOT NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT tracks_ranking_history_pk PRIMARY KEY (date, ranking),
	CONSTRAINT tracks_ranking_history_fk FOREIGN KEY (track_id) REFERENCES public.tracks(id)
);

CREATE TABLE public.artists_ranking (
	artist_id varchar NOT NULL,
	ranking int8 NOT NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT artists_ranking_pk PRIMARY KEY (ranking),
	CONSTRAINT artists_ranking_fk FOREIGN KEY (artist_id) REFERENCES public.artists(id)
);

CREATE TABLE public.artists_ranking_history (
	"date" date NOT NULL,
	ranking int8 NOT NULL,
	artist_id varchar NOT NULL,
	updated_at timestamp NULL DEFAULT now(),
	CONSTRAINT artists_ranking_history_pk PRIMARY KEY (date, ranking),
	CONSTRAINT artists_ranking_history_fk FOREIGN KEY (artist_id) REFERENCES public.artists(id)
);

-- Create tables in workspace

CREATE TABLE public.workspace_artists (
	id varchar NOT NULL,
	"name" varchar NULL,
	spotify_url varchar NULL,
	image_url varchar NULL,
	CONSTRAINT workspace_artists_pk PRIMARY KEY (id)
);

CREATE TABLE public.workspace_tracks (
	id varchar NOT NULL,
	artist_id varchar NULL,
	album_id varchar NULL,
	"name" varchar NULL,
	artist varchar NULL,
	spotify_url varchar NULL,
	album_image_url varchar NULL,
	CONSTRAINT workspace_tracks_pk PRIMARY KEY (id)
);
-- Create Views
CREATE 
OR REPLACE VIEW public.artists_time_in_top AS WITH artists AS 
(
   SELECT
      * 
   FROM
      public.artists_ranking_history trh 
      LEFT JOIN
         public.artists t 
         ON trh.artist_id = t.id 
)
SELECT
   artist_id id,
   name,
   image_url,
   COUNT(DISTINCT DATE) AS COUNT 
FROM
   artists t 
WHERE
   ranking <= 3 
   AND image_url IS NOT NULL 
   AND name IS NOT NULL 
GROUP BY
   1,2,3 
ORDER BY
   4 DESC,
   2 ASC LIMIT 10;

CREATE 
OR REPLACE VIEW public.tracks_time_in_top AS WITH tracks AS 
(
   SELECT
      trh.*,
      t.name,
      a.image_url 
   FROM
      public.tracks_ranking_history trh 
      LEFT JOIN
         public.tracks t 
         ON trh.track_id = t.id 
      LEFT JOIN
         public.artists a 
         ON a.id = t.artist_id 
)
SELECT
   track_id id,
   name,
   image_url,
   COUNT(DISTINCT DATE) 
FROM
   tracks t 
WHERE
   ranking <= 3 
   AND image_url NOTNULL 
GROUP BY
   1,2,3 
ORDER BY
   4 DESC,
   2 ASC LIMIT 10;

CREATE OR REPLACE VIEW public.artists_time_in_top_details
AS WITH artists AS (
         SELECT trh.date,
            trh.ranking,
            trh.artist_id,
            trh.updated_at,
            t_1.id,
            t_1.name,
            t_1.spotify_url,
            t_1.image_url,
            t_1.updated_at
           FROM artists_ranking_history trh
             LEFT JOIN public.artists t_1 ON trh.artist_id::text = t_1.id::text
        )
 SELECT t.artist_id AS id,
    t.name,
    t.image_url,
    count(DISTINCT t.date) AS count_total,
    count(DISTINCT t.date) FILTER (WHERE t.date >= (CURRENT_DATE - '7 days'::interval)) AS count_last_7,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '7 days'::interval) AND t.date >= (CURRENT_DATE - '1 mon'::interval)) AS count_last_30,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '1 mon'::interval) AND t.date >= (CURRENT_DATE - '2 mons'::interval)) AS count_last_60,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '2 mons'::interval)) AS count_prev
   FROM artists t(date, ranking, artist_id, updated_at, id, name, spotify_url, image_url, updated_at_1)
  WHERE t.ranking <= 3 AND t.image_url IS NOT NULL AND t.name IS NOT NULL
  GROUP BY t.artist_id, t.name, t.image_url
  ORDER BY (count(DISTINCT t.date)) DESC, t.name;
  
CREATE OR REPLACE VIEW public.tracks_time_in_top_details
AS WITH tracks AS (
         SELECT trh.date,
            trh.ranking,
            trh.track_id,
            trh.updated_at,
            t_1.name,
            a.image_url
           FROM tracks_ranking_history trh
             LEFT JOIN public.tracks t_1 ON trh.track_id::text = t_1.id::text
             LEFT JOIN artists a ON a.id::text = t_1.artist_id::text
        )
 SELECT t.track_id AS id,
    t.name,
    t.image_url,
    count(DISTINCT t.date) AS count_total,
    count(DISTINCT t.date) FILTER (WHERE t.date >= (CURRENT_DATE - '7 days'::interval)) AS count_last_7,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '7 days'::interval) AND t.date >= (CURRENT_DATE - '1 mon'::interval)) AS count_last_30,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '1 mon'::interval) AND t.date >= (CURRENT_DATE - '2 mons'::interval)) AS count_last_60,
    count(DISTINCT t.date) FILTER (WHERE t.date < (CURRENT_DATE - '2 mons'::interval)) AS count_prev
   FROM tracks t
  WHERE t.ranking <= 3 AND t.image_url IS NOT NULL
  GROUP BY t.track_id, t.name, t.image_url
  ORDER BY (count(DISTINCT t.date)) DESC, t.name;