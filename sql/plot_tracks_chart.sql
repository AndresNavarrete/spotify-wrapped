select
    "date",
    "ranking",
    a."name" as "track",
    a.album_image_url as "album_image_url"
from
    public.tracks_ranking_history arh
left join public.tracks a on
    a.id = arh.track_id
where
    track_id  in (
    select
        track_id  
    from
        public.tracks_ranking ar left join public.tracks a2 on a2.id = ar.track_id  
    where
        ranking <= 8 and  
        a2.album_image_url  notnull
        )
order by
    3 ,
    1  