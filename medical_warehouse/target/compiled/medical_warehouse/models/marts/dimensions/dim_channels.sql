with source as (

    select
        channel_name
    from "medical_warehouse"."public_staging"."stg_telegram_messages"
    where channel_name is not null

),

deduplicated as (

    select distinct
        channel_name
    from source

)

select
    md5(cast(coalesce(cast(channel_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as channel_pk,
    channel_name
from deduplicated