select ts, json_extract(content, '$.title') from news_data_table
where json_extract(content, '$.title') like '%美股%'
order by ts
limit 1000


SELECT ts, json_extract(content, '$.title') FROM news_data_table WHERE ts >= '2020-01-01 00:00:00' 
AND ts <='2021-01-01 00:00:00' 
order by ts