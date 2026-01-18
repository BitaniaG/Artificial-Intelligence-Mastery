with source as (

    select
        id,
        channel_name,
        sender_id,
        message_text,
        message_date,
        raw_json
    from raw.telegram_messages

),

cleaned as (

    select
        cast(id as bigint)                    as message_pk,
        trim(channel_name)                    as channel_name,
        cast(sender_id as bigint)             as sender_id,
        cast(message_date as timestamp)       as message_date,
        nullif(trim(message_text), '')        as message_text,
        raw_json
    from source

)

select *
from cleaned
