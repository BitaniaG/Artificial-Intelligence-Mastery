with messages as (

    select
        message_pk,
        channel_name,
        message_date,
        sender_id,
        message_text
    from "medical_warehouse"."public_staging"."stg_telegram_messages"
    where message_date is not null

),

channels as (

    select
        channel_pk,
        channel_name
    from "medical_warehouse"."public_marts"."dim_channels"

)

select
    m.message_pk,
    c.channel_pk,
    m.message_date,
    m.sender_id,
    m.message_text
from messages m
left join channels c
    on m.channel_name = c.channel_name