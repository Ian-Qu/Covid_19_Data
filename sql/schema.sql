CREATE TABLE IF NOT EXISTS state_daily_metrics (
    date TEXT NOT NULL,
    state_code TEXT NOT NULL,
    state_name TEXT NOT NULL,
    total_positive REAL,
    total_negative REAL,
    total_tests REAL,
    hospitalized_currently REAL,
    total_deaths REAL,
    new_positive_cases REAL,
    new_negative_tests REAL,
    new_deaths REAL,
    PRIMARY KEY (date, state_code)
);
CREATE INDEX IF NOT EXISTS idx_state_daily_metrics_state_date ON state_daily_metrics(state_code, date);
