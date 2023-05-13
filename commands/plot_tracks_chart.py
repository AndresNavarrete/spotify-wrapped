from src.content_generator import ContentGenerator

if __name__ == "__main__":
    items_name = "track"
    item_url_name = "album_image_url"
    query = """
    select
        "date",
        "ranking",
        a."name" as "track",
        a.album_image_url as "album_image_url"
    from
        dev.tracks_ranking_history arh
    left join dev.tracks a on
        a.id = arh.track_id
    where
        track_id  in (
        select
            track_id  
        from
            dev.tracks_ranking ar left join dev.tracks a2 on a2.id = ar.track_id  
        where
            ranking <= 7 and  
            a2.album_image_url  notnull
            )
    order by
        3 ,
        1    
    """    
    ContentGenerator(query, items_name, item_url_name).make_chart()
