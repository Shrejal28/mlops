
import os
import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

ref = pd.read_csv("reference.csv")
cur = pd.read_csv("current.csv")

report = Report(metrics=[DataDriftPreset()])
result = report.run(current_data=cur, reference_data=ref)

os.makedirs("reports", exist_ok=True)
result.save_html("reports/drift_report.html")

metrics = result.dict()["metrics"]

for metric in metrics:
    if "DriftedColumnsCount" in metric.get("metric_name", ""):
        values = metric["value"]
        print("Columns drifted:", values.get("count"), "/", values.get("total"))

    if "DatasetDriftMetric" in metric.get("metric_name", ""):
        print("Dataset drift  :", metric.get("value"))

print("Report saved   : reports/drift_report.html")
