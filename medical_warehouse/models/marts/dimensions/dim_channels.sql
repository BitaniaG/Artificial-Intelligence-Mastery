with source as (

    select
        channel_name
    from {{ ref('stg_telegram_messages') }}
    where channel_name is not null

),

deduplicated as (

    select distinct
        channel_name
    from source

)

select
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_pk,
    channel_name
from deduplicated
