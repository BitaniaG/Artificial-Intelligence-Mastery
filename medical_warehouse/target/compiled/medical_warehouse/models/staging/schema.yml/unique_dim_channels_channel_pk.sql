
    
    

select
    channel_pk as unique_field,
    count(*) as n_records

from "medical_warehouse"."public_marts"."dim_channels"
where channel_pk is not null
group by channel_pk
having count(*) > 1


