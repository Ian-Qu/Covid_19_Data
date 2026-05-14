import pandas as pd
from pathlib import Path

RAW_PATH = Path('data/raw/us_states_covid19_daily.csv')
PROCESSED_PATH = Path('data/processed/covid_state_clean.csv')

COLUMN_MAP = {
    'date': 'date',
    'state': 'state_code',
    'positive': 'total_positive',
    'negative': 'total_negative',
    'totalTestResults': 'total_tests',
    'hospitalizedCurrently': 'hospitalized_currently',
    'death': 'total_deaths',
    'positiveIncrease': 'new_positive_cases',
    'negativeIncrease': 'new_negative_tests',
    'deathIncrease': 'new_deaths'
}

STATE_NAMES = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    'DC': 'District of Columbia'
}

def load_data(path=RAW_PATH):
    return pd.read_csv(path)

def clean_data(df):
    df = df.copy()
    selected = df[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP)
    selected['date'] = pd.to_datetime(selected['date'].astype(str), format='%Y%m%d', errors='coerce')
    numeric_cols = ['total_positive', 'total_negative', 'total_tests', 'hospitalized_currently', 'total_deaths', 'new_positive_cases', 'new_negative_tests', 'new_deaths']
    for col in numeric_cols:
        selected[col] = pd.to_numeric(selected[col], errors='coerce').fillna(0)
    selected['state_code'] = selected['state_code'].astype(str).str.strip().str.upper()
    selected['state_name'] = selected['state_code'].map(STATE_NAMES).fillna(selected['state_code'])
    selected = selected.dropna(subset=['date', 'state_code'])
    selected = selected.sort_values(['state_code', 'date'])
    return selected[['date', 'state_code', 'state_name', 'total_positive', 'total_negative', 'total_tests', 'hospitalized_currently', 'total_deaths', 'new_positive_cases', 'new_negative_tests', 'new_deaths']]

def save_clean_data(df, path=PROCESSED_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

def main():
    df = load_data()
    clean_df = clean_data(df)
    save_clean_data(clean_df)
    print(f'Saved {len(clean_df)} cleaned rows to {PROCESSED_PATH}')

if __name__ == '__main__':
    main()
