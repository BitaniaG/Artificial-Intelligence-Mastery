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
