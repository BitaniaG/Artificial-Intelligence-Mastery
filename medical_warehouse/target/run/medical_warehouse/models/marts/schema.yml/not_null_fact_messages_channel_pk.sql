
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel_pk
from "medical_warehouse"."public_marts"."fact_messages"
where channel_pk is null



  
  
      
    ) dbt_internal_test