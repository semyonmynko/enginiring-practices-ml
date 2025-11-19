import mlflow

runs = mlflow.search_runs()

cols_to_show = [
    "run_id",
    "metrics.accuracy",
    "params.model",
    "params.model_name",
    "params.model_type",
    "metrics.training_time",
]

existing_cols = [c for c in cols_to_show if c in runs.columns]

print("\nТоп-5 экспериментов по accuracy:\n")
if "metrics.accuracy" in runs.columns:
    df_view = (
        runs[existing_cols].sort_values("metrics.accuracy", ascending=False).head(5)
    )
else:
    df_view = runs[existing_cols].head(5)

print(df_view)

if "metrics.accuracy" in runs.columns:
    print("\nЭксперименты с accuracy > 0.9 и < 1:\n")
    high_acc = (
        runs[(runs["metrics.accuracy"] > 0.9) & (runs["metrics.accuracy"] != 1)]
        .sort_values("metrics.accuracy", ascending=False)
        .head(10)
    )
    print(high_acc[existing_cols])

if "metrics.accuracy" in runs.columns:
    print("\nЭксперименты с training_time > 0.3:\n")
    high_acc = runs[runs["metrics.training_time"] > 0.3]
    print(high_acc[existing_cols])
