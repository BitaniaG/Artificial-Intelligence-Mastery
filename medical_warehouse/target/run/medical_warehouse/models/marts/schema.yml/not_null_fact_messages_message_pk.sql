
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select message_pk
from "medical_warehouse"."public_marts"."fact_messages"
where message_pk is null



  
  
      
    ) dbt_internal_test