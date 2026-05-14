-- Peak total positive cases by state
SELECT state_name, MAX(total_positive) AS peak_total_positive
FROM state_daily_metrics
GROUP BY state_name
ORDER BY peak_total_positive DESC;

-- New Jersey daily trend
SELECT date, state_name, new_positive_cases, new_deaths
FROM state_daily_metrics
WHERE state_code = 'NJ'
ORDER BY date;

-- Highest single day new cases
SELECT state_name, date, new_positive_cases
FROM state_daily_metrics
ORDER BY new_positive_cases DESC
LIMIT 10;

-- Compare selected states by new positive cases
SELECT date, state_name, new_positive_cases
FROM state_daily_metrics
WHERE state_name IN ('New Jersey', 'New York', 'Pennsylvania')
ORDER BY date;
