# Artificial-Intelligence-Mastery
Shipping a Data Product: From Raw Telegram Data to an Analytical API
# Task 1 – Data Scraping and Collection

## Overview

This task focuses on building the **Extract & Load (EL)** part of an end-to-end data pipeline. The objective is to collect raw data from public Telegram channels related to medical and pharmaceutical products in Ethiopia and store it in a structured **data lake** without modifying or cleaning the data.

At this stage, the goal is **data reliability and reproducibility**, not analysis. All data is stored in its original form so that downstream transformations can be applied safely.

---

## Business Context

Kara Solutions aims to generate insights about Ethiopian medical businesses using publicly available Telegram data. Telegram channels are widely used to advertise pharmaceuticals, cosmetics, and medical products. Capturing this data enables later analysis such as:

* Product popularity
* Channel activity trends
* Visual vs text-based marketing patterns

Task 1 lays the foundation for all subsequent tasks.

---

## Data Sources

Public Telegram channels scraped in this task include:

* **Lobelia Cosmetics** (`lobelia4cosmetics`)
* **Tikvah Pharma** (`tikvahpharma`)

Additional channels can be added later from: [https://et.tgstat.com/medicine](https://et.tgstat.com/medicine)

---

## Data Collected

For each Telegram message, the following fields are extracted:

* `message_id` – Unique identifier of the message
* `channel_name` – Telegram channel name
* `message_date` – Timestamp of the message
* `message_text` – Text content of the message
* `views` – Number of views
* `forwards` – Number of forwards
* `has_media` – Whether the message contains media
* `image_path` – Local path to downloaded image (if applicable)

When a message contains an image, the image is downloaded and stored locally.

---

## Folder Structure

The data lake follows a partitioned and organized structure:

```
medical-telegram-warehouse/
├── data/
│   └── raw/
│       ├── telegram_messages/
│       │   └── YYYY-MM-DD/
│       │       ├── lobelia4cosmetics.json
│       │       └── tikvahpharma.json
│       └── images/
│           ├── lobelia4cosmetics/
│           │   └── <message_id>.jpg
│           └── tikvahpharma/
│               └── <message_id>.jpg
├── logs/
│   └── scraper.log
├── src/
│   └── scraper.py
├── .env
├── requirements.txt
└── README.md
```

---

## Implementation Details

### Environment Setup

* Telegram API credentials (`api_id`, `api_hash`) are stored securely in a `.env` file.
* Dependencies are managed using `requirements.txt`.
* A virtual environment is recommended.

### Scraping Logic

* The **Telethon** library is used to connect to the Telegram API.
* Messages are scraped using `iter_messages()` with a controlled limit to avoid excessive historical downloads.
* Images are downloaded only when media is present.
* Raw data is stored as JSON files without transformation.

### Logging

* Scraping activity and errors are logged to `logs/scraper.log`.
* Logs include channel start, completion, and message counts.

---

## Output and Validation

A successful run of Task 1 produces:

* JSON files containing raw Telegram messages
* Image files organized by channel
* A populated log file confirming scraping activity
* A Telegram session file (`.session`) stored locally for authentication reuse

No data cleaning or transformation is performed at this stage.

---

## Key Learnings

* Secure handling of API credentials
* Designing a scalable data lake structure
* Scraping unstructured data from real-world sources
* Managing long-running data collection processes
* Importance of logging and reproducibility

---

## Next Steps

The raw data generated in Task 1 will be loaded into PostgreSQL in **Task 2**, where transformations and analytical modeling will be implemented using **dbt**.


# Task 2 — Data Warehouse & Analytics (dbt)

## Objective
Transform raw Telegram message data into a clean, testable, analytics-ready
data warehouse using dbt and PostgreSQL.

---

## Project Structure

medical_warehouse/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/
│   │   ├── stg_telegram_messages.sql
│   │   └── schema.yml
│   └── marts/
│       ├── dimensions/
│       │   └── dim_channels.sql
│       └── facts/
│           └── fact_messages.sql
└── tests/

---

## Data Models

### Staging
- `stg_telegram_messages`
  - Cleans raw data
  - Generates surrogate primary keys
  - Standardizes column names

### Dimensions
- `dim_channels`
  - One row per Telegram channel
  - Uses surrogate key (`channel_pk`)

### Facts
- `fact_messages`
  - One row per Telegram message
  - Links to `dim_channels`
  - Filters invalid records (null dates)

---

## Data Quality
All models are tested using dbt tests:
- Primary keys: `not_null`, `unique`
- Foreign keys: `not_null`
- Core fields validated

```bash
dbt test --profiles-dir .


📷 Task 3 — Image Data Enrichment with YOLOv8
Overview

Task 3 extends the Telegram data platform by enriching scraped image data with computer vision insights. Using YOLOv8 object detection, images from Ethiopian medical Telegram channels are analyzed to identify objects such as products, people, and packaging. The detection results are integrated into the PostgreSQL data warehouse using dbt, enabling advanced visual content analytics.

Objectives

Detect objects in Telegram images using YOLOv8

Store detection results in a structured format (CSV)

Integrate image detections into the data warehouse

Enable analytics on visual content patterns across channels

Folder Structure:
src/
└── vision/
    └── yolo_inference.py

data/
├── raw/
│   └── telegram/
│       └── images/
│           ├── lobelia4cosmetics/
│           └── tikvahpharma/
├── enriched/
│   └── image_detections/
│       ├── detections.json
│       └── detections.csv

medical_warehouse/
├── seeds/
│   └── image_detections.csv
├── models/
│   ├── staging/
│   │   └── stg_image_detections.sql
│   └── marts/
│       └── facts/
│           └── fct_image_detections.sql

Object Detection Pipeline
1. YOLO Inference

The script src/vision/yolo_inference.py:

Loads a pre-trained YOLOv8 model

Iterates through Telegram images by channel

Detects objects per image

Saves detection results with:

channel_name

image_name

object_class

confidence

bounding box coordinates

Output:

detections.json

detections.csv

2. Data Warehouse Integration

The detection CSV is loaded into PostgreSQL using dbt seeds:

dbt seed


Two dbt models are then created:

stg_image_detections

Cleans and standardizes detection data

Casts numeric fields

Prepares data for analytics

fct_image_detections

Fact table containing one row per detected object

Enables joins with message and channel dimensions

Supports image-based analytics

Data Quality & Testing

The following dbt tests are implemented:

not_null on key fields (channel, image_name, object_class)

Valid numeric confidence values

Referential integrity where applicable

All tests pass successfully using:

dbt test

Analytical Use Cases Enabled

The enriched dataset enables insights such as:

Most common object types in medical advertisements

Visual content distribution by Telegram channel

Comparison of product-focused vs lifestyle-focused imagery

Confidence analysis of detected objects

These insights enhance understanding of how Ethiopian medical businesses visually market their products on Telegram.

TASK 4 — FastAPI Analytics API
Overview

Task 4 exposes the analytical warehouse built in previous tasks through a production-ready REST API using FastAPI.
The API provides programmatic access to curated dbt models, enabling downstream applications, dashboards, and analytics consumers to query Telegram data and image detection insights.

This task completes the data → warehouse → API pipeline.

Architecture:
PostgreSQL (Warehouse)
   │
   ├── dim_channels
   ├── fact_messages
   ├── fct_image_detections
   │
FastAPI (src/api)
   │
   ├── /channels
   ├── /messages
   └── /image-detections

folder structure:
src/
└── api/
    ├── main.py              # FastAPI application entry point
    ├── database.py          # SQLAlchemy database connection
    ├── routers/
    │   ├── channels.py      # Channel endpoints
    │   ├── messages.py      # Message endpoints
    │   ├── images.py        # Image detection endpoints
    │   └── __init__.py
    └── __init__.py
src/
└── api/
    ├── main.py              # FastAPI application entry point
    ├── database.py          # SQLAlchemy database connection
    ├── routers/
    │   ├── channels.py      # Channel endpoints
    │   ├── messages.py      # Message endpoints
    │   ├── images.py        # Image detection endpoints
    │   └── __init__.py
    └── __init__.py

Environment Configuration
Create a .env file in the project root:
DB_HOST=localhost
DB_PORT=5433
DB_USER=postgres
DB_PASSWORD=your_actual_password
DB_NAME=medical_warehouse
Passwords containing special characters are safely encoded using quote_plus.

Running the API
From the project root:
python -m uvicorn src.api.main:app --reload

The API will be available at:
Base URL: http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs

Available Endpoints
🔹 Channels
GET /channels
Returns all Telegram channels in the warehouse.

🔹 Messages
GET /messages?limit=100
Returns recent messages across all channels.

🔹 Image Detections
GET /image-detections
Returns YOLO object detection results linked to Telegram images.

Verification

Successful setup is confirmed when:

API starts without import errors

Swagger UI loads

All endpoints return data from PostgreSQL

Task 5 — Pipeline Orchestration with Dagster
Overview

Task 5 introduces workflow orchestration using Dagster to automate the end-to-end data pipeline built in previous tasks.
The Dagster pipeline ensures reliable, repeatable execution of data ingestion, transformation, enrichment, and analytics.

Pipeline Stages:
Telegram Scraping
      ↓
Load Raw Data to PostgreSQL
      ↓
dbt Transformations (Staging → Marts)
      ↓
YOLO Image Enrichment
      ↓
Analytics API Ready

folder structure : 
dagster/
├── __init__.py
├── ops.py          # Pipeline operations
├── jobs.py         # Dagster job definitions
├── schedules.py    # Scheduled runs
└── repository.py   # Dagster repository

Defined Ops:
  Op	Description
scrape_telegram_data	Runs Telethon scraper
load_raw_to_postgres	Loads JSON into PostgreSQL
run_dbt_models	Executes dbt run + test
run_yolo_enrichment	Runs YOLO detection pipeline

Dagster job 
telegram_analytics_job = job(
    ops=[
        scrape_telegram_data,
        load_raw_to_postgres,
        run_dbt_models,
        run_yolo_enrichment
    ]
)

Scheduling

Daily scheduled execution using Dagster ScheduleDefinition

Ensures continuous refresh of insights

Running Dagster
dagster dev

Open UI at:

http://localhost:3000

Deliverables

Dagster job definition

Ops with clear dependencies

Scheduled execution

UI screenshots showing successful runs
