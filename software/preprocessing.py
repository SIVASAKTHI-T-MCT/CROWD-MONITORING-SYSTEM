import json, glob, os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from utils import polar_to_xy

DATA_DIR = "../data/raw"
OUT_FILE = "../ml_model/dataset.jsonl"
EPS = 0.2  # meters; tune for your setup
MIN_SAMPLES = 3

def label_sweep(fname):
    with open(fname) as f:
        sweep = json.load(f)
    pts = polar_to_xy(sweep["angles"], sweep["distances"])
    if pts.shape[0] == 0:
        return []
    db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLES).fit(pts)
    labels = db.labels_
    unique = set(labels)
    labeled = []
    for lab in sorted(unique):
        if lab == -1: continue
        mask = labels == lab
        cluster_pts = pts[mask]
        plt.figure(figsize=(4,4))
        plt.scatter(pts[:,0], pts[:,1], s=8)
        plt.scatter(cluster_pts[:,0], cluster_pts[:,1], s=20)
        plt.gca().set_aspect('equal', 'box')
        plt.title(f"{os.path.basename(fname)} cluster {lab}: {len(cluster_pts)} pts")
        plt.show()
        ans = input("Is this cluster human? (y/n) ")
        labeled.append({
            "file": fname,
            "cluster": int(lab),
            "n_points": int(len(cluster_pts)),
            "mean_dist_m": float(cluster_pts[:,0:].mean()),
            "is_human": ans.strip().lower().startswith('y')
        })
    return labeled

def main():
    files = glob.glob(os.path.join(DATA_DIR, "sweep_*.json"))
    with open(OUT_FILE, "a") as out:
        for f in files:
            labs = label_sweep(f)
            for L in labs:
                out.write(json.dumps(L) + "\n")
            print("done", f)

if __name__ == "__main__":
    main()
