with artists as (
	select
			*
	from
			dev.artists_ranking_history trh
	left join dev.artists t on
			trh.artist_id = t.id
)
select
	name,
	image_url,
	count(distinct date)
from
	artists t
where
	ranking <= 3
	and image_url notnull and name notnull 
group by
	1, 2
order by
	3 desc , 1 asc 
limit 10;