
    
    

with child as (
    select channel_pk as from_field
    from "medical_warehouse"."public_marts"."fact_messages"
    where channel_pk is not null
),

parent as (
    select channel_pk as to_field
    from "medical_warehouse"."public_marts"."dim_channels"
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


