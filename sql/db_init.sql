
-- Create schemas

CREATE SCHEMA dev;
CREATE SCHEMA workspace;
CREATE SCHEMA prod;

-- Create tables in dev

CREATE TABLE dev.artists (
	id varchar NOT NULL,
	"name" varchar NULL,
	spotify_url varchar NULL,
	image_url varchar NULL,
	CONSTRAINT artists_pk PRIMARY KEY (id)
);

CREATE TABLE dev.tracks (
	id varchar NOT NULL,
	artist_id varchar NULL,
	album_id varchar NULL,
	"name" varchar NULL,
	artist varchar NULL,
	spotify_url varchar NULL,
	album_image_url varchar NULL,
	CONSTRAINT tracks_pk PRIMARY KEY (id)
);

CREATE TABLE dev.tracks_ranking (
	track_id varchar NOT NULL,
	ranking int8 NOT NULL,
	CONSTRAINT tracks_ranking_pk PRIMARY KEY (ranking),
	CONSTRAINT tracks_ranking_fk FOREIGN KEY (track_id) REFERENCES dev.tracks(id)
);

CREATE TABLE dev.tracks_ranking_history (
	"date" date NOT NULL,
	ranking int8 NOT NULL,
	track_id varchar NOT NULL,
	CONSTRAINT tracks_ranking_history_pk PRIMARY KEY (date, ranking),
	CONSTRAINT tracks_ranking_history_fk FOREIGN KEY (track_id) REFERENCES dev.tracks(id)
);

-- Create tables in workspace

CREATE TABLE workspace.artists (
	id varchar NOT NULL,
	"name" varchar NULL,
	spotify_url varchar NULL,
	image_url varchar NULL,
	CONSTRAINT artists_pk PRIMARY KEY (id)
);

CREATE TABLE workspace.tracks (
	id varchar NOT NULL,
	artist_id varchar NULL,
	album_id varchar NULL,
	"name" varchar NULL,
	artist varchar NULL,
	spotify_url varchar NULL,
	album_image_url varchar NULL,
	CONSTRAINT tracks_pk PRIMARY KEY (id)
);