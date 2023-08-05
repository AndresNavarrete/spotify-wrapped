with tracks as (
	select
		trh.*,
		t.name,
		a.image_url
	from
		public.tracks_ranking_history trh
	left join public.tracks t on
		trh.track_id = t.id
	left join public.artists a on
		a.id = t.artist_id
)
select
	name,
	image_url,
	count(distinct date)
from
	tracks t
where
	ranking <= 3
	and image_url notnull
group by
	1 , 2
order by
	3 desc , 1 asc 
limit 10;