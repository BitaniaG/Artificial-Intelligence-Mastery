with dates as (

    select distinct
        cast(message_date as date) as date_day
    from {{ ref('stg_telegram_messages') }}
    where message_date is not null

)

select
    {{ dbt_utils.generate_surrogate_key(['date_day']) }} as date_pk,
    date_day,
    extract(year from date_day)  as year,
    extract(month from date_day) as month,
    extract(day from date_day)   as day,
    extract(dow from date_day)   as day_of_week
from dates
