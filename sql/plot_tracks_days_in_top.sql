with tracks as (
	select
		trh.*,
		t.name,
		a.image_url
	from
		dev.tracks_ranking_history trh
	left join dev.tracks t on
		trh.track_id = t.id
	left join dev.artists a on
		a.id = t.artist_id
)
select
	name,
	image_url,
	count(distinct date)
from
	tracks t
where
	ranking <= 10
	and image_url notnull
group by
	1 , 2
order by
	3 desc 
limit 10;