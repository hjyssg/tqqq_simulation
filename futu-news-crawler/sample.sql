with  Temp_Table AS (
    select *, json_extract(content, '$.title') as title, 
    json_extract(content, '$.url') as url  
    from news_data_table WHERE ts >= '2021/05/01 00:00:00' ) 


select * FROM Temp_Table
-- where content like '%大空头%'
order by ts
limit 1000


