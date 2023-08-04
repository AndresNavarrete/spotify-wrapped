
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