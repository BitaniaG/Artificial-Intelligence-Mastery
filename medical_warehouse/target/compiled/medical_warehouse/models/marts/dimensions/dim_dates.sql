with dates as (

    select distinct
        cast(message_date as date) as date_day
    from "medical_warehouse"."public_staging"."stg_telegram_messages"
    where message_date is not null

)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as date_pk,
    date_day,
    extract(year from date_day)  as year,
    extract(month from date_day) as month,
    extract(day from date_day)   as day,
    extract(dow from date_day)   as day_of_week
from dates