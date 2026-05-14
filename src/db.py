import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path('data/covid_state.db')
CLEAN_PATH = Path('data/processed/covid_state_clean.csv')
SCHEMA_PATH = Path('sql/schema.sql')

def get_connection(db_path=DB_PATH):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path)

def create_schema(conn, schema_path=SCHEMA_PATH):
    schema_sql = schema_path.read_text()
    conn.executescript(schema_sql)
    conn.commit()

def load_clean_csv(path=CLEAN_PATH):
    return pd.read_csv(path, parse_dates=['date'])

def insert_data(conn, df):
    rows = df.copy()
    rows['date'] = rows['date'].dt.strftime('%Y-%m-%d')
    rows.to_sql('state_daily_metrics', conn, if_exists='append', index=False)
    conn.commit()

def main():
    conn = get_connection()
    create_schema(conn)
    df = load_clean_csv()
    insert_data(conn, df)
    conn.close()
    print(f'Loaded {len(df)} rows into {DB_PATH}')

if __name__ == '__main__':
    main()
