# train_model.py
import json, glob, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from joblib import dump
import os

# Read cluster labels from CSV
dataset_path = "dataset.csv"
df = pd.read_csv(dataset_path)

# Feature vector for classifier: [n_points, mean_dist_m]
X = df[["n_points", "mean_dist_m"]].values
y = df["is_human"].astype(int).values

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)
dump(clf, "human_cluster_clf.joblib")
print("Saved human_cluster_clf.joblib")

# For counting: aggregate by file
# Note: we need the original cluster features to aggregate accurately
# If we only have the CSV, we can group by 'file'
sweep_agg = df.groupby("file").agg({
    "cluster": "count",
    "n_points": "sum",
    "mean_dist_m": "mean",
    "is_human": "sum"
}).rename(columns={"cluster": "num_clusters", "is_human": "humans"})

X_s = sweep_agg[["num_clusters", "n_points", "mean_dist_m"]].values
y_s = sweep_agg["humans"].values

reg = RandomForestRegressor(n_estimators=100, random_state=42)
reg.fit(X_s, y_s)
dump(reg, "count_regressor.joblib")
print("Saved count_regressor.joblib")

# Generate metrics for Results
from sklearn.metrics import accuracy_score, mean_absolute_error
y_pred_clf = clf.predict(X)
acc = accuracy_score(y, y_pred_clf)
y_pred_reg = reg.predict(X_s)
mae = mean_absolute_error(y_s, y_pred_reg)

results_dir = "../results"
os.makedirs(results_dir, exist_ok=True)
with open(os.path.join(results_dir, "accuracy_metrics.txt"), "w") as f:
    f.write(f"Human Classification Accuracy: {acc:.4f}\n")
    f.write(f"Count Regression MAE: {mae:.4f}\n")
print(f"Metrics saved to {results_dir}/accuracy_metrics.txt")
