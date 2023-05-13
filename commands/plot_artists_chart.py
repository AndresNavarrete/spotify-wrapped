from src.content_generator import ContentGenerator

if __name__ == "__main__":
    items_name = "artist"
    item_url_name = "artist_image_url"
    query = """
    select
        "date",
        "ranking",
        a."name" as "artist",
        a.image_url as "artist_image_url"
    from
        dev.artists_ranking_history arh
    left join dev.artists a on
        a.id = arh.artist_id
    where
        artist_id in (
        select
            artist_id 
        from
            dev.artists_ranking ar left join dev.artists a2 on a2.id = ar.artist_id  
        where
            ranking <= 7 and  
            a2.image_url notnull
            )
    order by
        3 ,
        1   
    """    
    ContentGenerator(query, items_name, item_url_name).make_chart()
