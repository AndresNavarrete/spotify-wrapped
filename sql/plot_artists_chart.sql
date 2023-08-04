select
    "date",
    "ranking",
    a."name" as "artist",
    a.image_url as "artist_image_url"
from
    public.artists_ranking_history arh
left join public.artists a on
    a.id = arh.artist_id
where
    artist_id in (
    select
        artist_id 
    from
        public.artists_ranking ar left join public.artists a2 on a2.id = ar.artist_id  
    where
        ranking <= 8 and  
        a2.image_url notnull
        )
order by
    3 ,
    1  
