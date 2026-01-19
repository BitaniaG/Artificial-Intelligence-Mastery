
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    channel_pk as unique_field,
    count(*) as n_records

from "medical_warehouse"."public_marts"."dim_channels"
where channel_pk is not null
group by channel_pk
having count(*) > 1



  
  
      
    ) dbt_internal_test