import sqlite3
import pandas as pd
import streamlit as st
import altair as alt

DB_PATH = 'data/covid_state.db'

st.set_page_config(page_title="US COVID State Dashboard (2020 Only)", layout="wide")
st.title("US COVID State Dashboard (2020 Only)")
st.caption("Interactive dashboard for state-level COVID-19 trends in 2020 only.")

@st.cache_data
def load_states():
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query('SELECT DISTINCT state_name FROM state_daily_metrics ORDER BY state_name', conn)
    return df['state_name'].tolist()

@st.cache_data
def load_state_data(state_name):
    query = 'SELECT date, state_code, state_name, total_positive, total_negative, total_tests, hospitalized_currently, total_deaths, new_positive_cases, new_negative_tests, new_deaths FROM state_daily_metrics WHERE state_name = ? ORDER BY date'
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn, params=(state_name,))
    df['date'] = pd.to_datetime(df['date'])
    return df

@st.cache_data
def load_multi_state_data(selected_states, metric):
    placeholders = ','.join(['?'] * len(selected_states))
    query = f'SELECT date, state_name, {metric} FROM state_daily_metrics WHERE state_name IN ({placeholders}) ORDER BY date'
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn, params=selected_states)
    df['date'] = pd.to_datetime(df['date'])
    return df

states = load_states()
if not states:
    st.warning('No state data found. Run ETL and database load first.')
    st.stop()

selected_state = st.selectbox('Select a state', states, index=states.index('New Jersey') if 'New Jersey' in states else 0)
df = load_state_data(selected_state)

st.subheader('Single State View')
col1, col2, col3 = st.columns(3)
col1.metric('Latest total positive', f"{int(df['total_positive'].iloc[-1]):,}" if not df.empty else 'N/A')
col2.metric('Latest total deaths', f"{int(df['total_deaths'].iloc[-1]):,}" if not df.empty else 'N/A')
col3.metric('Latest hospitalized', f"{int(df['hospitalized_currently'].iloc[-1]):,}" if not df.empty else 'N/A')

chart_metric = st.selectbox('Choose single state metric', ['new_positive_cases', 'new_deaths', 'hospitalized_currently', 'total_tests'])
line = alt.Chart(df).mark_line().encode(
    x='date:T',
    y=alt.Y(f'{chart_metric}:Q', title=chart_metric.replace('_', ' ').title()),
    tooltip=['date:T', 'state_name:N', alt.Tooltip(f'{chart_metric}:Q', title='Value')]
).properties(height=400, title=f'{selected_state} {chart_metric.replace("_", " ").title()} Over Time')
st.altair_chart(line, use_container_width=True)
st.dataframe(df.tail(30), use_container_width=True)

st.subheader('State to State Comparison')
compare_states = st.multiselect(
    'Select up to 5 states to compare',
    states,
    default=['New Jersey', 'New York'] if 'New Jersey' in states and 'New York' in states else states[:2],
    max_selections=5
)
compare_metric = st.selectbox('Choose comparison metric', ['new_positive_cases', 'new_deaths', 'hospitalized_currently', 'total_tests'], key='compare_metric')

if compare_states:
    compare_df = load_multi_state_data(compare_states, compare_metric)
    comparison_chart = alt.Chart(compare_df).mark_line().encode(
        x='date:T',
        y=alt.Y(f'{compare_metric}:Q', title=compare_metric.replace('_', ' ').title()),
        color='state_name:N',
        tooltip=['date:T', 'state_name:N', alt.Tooltip(f'{compare_metric}:Q', title='Value')]
    ).properties(height=450, title=f'State Comparison: {compare_metric.replace("_", " ").title()}')
    st.altair_chart(comparison_chart, use_container_width=True)
    st.dataframe(compare_df.tail(50), use_container_width=True)
else:
    st.info('Select at least one state to compare.')
