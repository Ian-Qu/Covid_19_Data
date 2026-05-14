# US COVID State Dashboard (2020 Only)

Kaggle source: https://www.kaggle.com/datasets/sudalairajkumar/covid19-in-usa?select=us_states_covid19_daily.csv

This project is a Python, SQL, and Streamlit analytics workflow built from historical U.S. state-level COVID-19 data for 2020 only. It cleans the raw CSV, stores the transformed data in SQLite, and provides an interactive dashboard for state-level trend analysis and multi-state comparison.

## Program purpose
This project is designed to show how Python can be used for more than charting alone. It demonstrates the full lifecycle of a small analytics application, from raw data ingestion to cleaned storage to user facing visual exploration.

## What users can do
Visitors to the GitHub repository can understand the project in two ways:
- Read the README to see the project goal, data flow, and technical stack.
- Run the Streamlit dashboard locally to interact with the data.

Once the dashboard is running, users can:
- Select a single state and view key COVID metrics over time.
- Compare up to 5 states on the same chart.
- Switch between metrics such as new positive cases, deaths, hospitalizations, and total tests.
- Review recent underlying records in table form.

## Dataset focus
The original CSV contains many columns, but this project focuses on the most useful state level metrics:
- `date`
- `state`
- `positive`
- `negative`
- `totalTestResults`
- `hospitalizedCurrently`
- `death`
- `positiveIncrease`
- `negativeIncrease`
- `deathIncrease`

These are cleaned and renamed into:
- `date`
- `state_code`
- `state_name`
- `total_positive`
- `total_negative`
- `total_tests`
- `hospitalized_currently`
- `total_deaths`
- `new_positive_cases`
- `new_negative_tests`
- `new_deaths`

## Folder structure
```text
data/
  processed/
    covid_state_clean.csv
  raw/
    us_states_covid19_daily.csv
sql/
  queries.sql
  schema.sql
src/
  app.py
  db.py
  etl.py
README.md
requirements.txt
```