
  create view "medical_warehouse"."public_staging"."stg_image_detections__dbt_tmp"
    
    
  as (
    with source as (

    select
        channel_name,
        image_name,
        object_class,
        confidence::float as confidence,
        x_min::float as x_min,
        y_min::float as y_min,
        x_max::float as x_max,
        y_max::float as y_max
    from "medical_warehouse"."public"."image_detections"

)

select *
from source
  );