select
    row_number() over () as detection_pk,
    channel_name,
    image_name,
    object_class,
    confidence,
    x_min,
    y_min,
    x_max,
    y_max
from {{ ref('stg_image_detections') }}
