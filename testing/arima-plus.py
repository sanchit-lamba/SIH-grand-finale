from google.cloud import bigquery
client = bigquery.Client(project="gen-lang-client-0429922721")

evaluate_query = """
SELECT *
FROM ML.EVALUATE(MODEL `gen-lang-client-0429922721.out.arima_plus_model`,
(
  SELECT DateTime, DELHI
  FROM `gen-lang-client-0429922721.out.csv`
  WHERE DateTime BETWEEN '2024-06-07' AND '2024-11-12'
))
"""
# Step 3: Forecast future values
# Set horizon as needed. For example, forecasting the next 288 intervals (assuming 5-min intervals for one day):
forecast_query = """
SELECT
  *
FROM ML.FORECAST(MODEL `gen-lang-client-0429922721.out.arima_plus_model`,
                 STRUCT(63360 AS horizon, 0.8 AS confidence_level))
"""
print("Evaluating the model...")
eval_job = client.query(evaluate_query)
eval_results = eval_job.result().to_dataframe()
print("Evaluation Results:")
print(eval_results)
print("\n")



