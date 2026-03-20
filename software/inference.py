# inference.py
import serial, json, joblib, numpy as np, time
from sklearn.cluster import DBSCAN
from collections import defaultdict
from utils import polar_to_xy

# Update paths to relative to current structure or pass as args
CLF_PATH = "../ml_model/human_cluster_clf.joblib"
REG_PATH = "../ml_model/count_regressor.joblib"

ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
clf = joblib.load(CLF_PATH)
reg = joblib.load(REG_PATH)

sweeps = {}
while True:
    line = ser.readline().decode('utf-8', errors='ignore').strip()
    if not line: continue
    try:
        obj = json.loads(line)
    except:
        continue
    sid = obj["sweep_id"]
    if sid not in sweeps:
        sweeps[sid] = {"angles":[],"distances":[]}
    sweeps[sid]["angles"].append(obj["angle"])
    sweeps[sid]["distances"].append(obj["distance_cm"])
    # flush when angle==180 (end of sweep)
    if obj["angle"] == 180:
        s = sweeps.pop(sid)
        pts = polar_to_xy(s["angles"], s["distances"])
        if pts.shape[0] == 0:
            print("No points")
            continue
        db = DBSCAN(eps=0.2, min_samples=3).fit(pts)
        labs = db.labels_
        human_count = 0
        cluster_feats = []
        for lab in set(labs):
            if lab == -1: continue
            mask = labs==lab
            cluster_pts = pts[mask]
            feat = [len(cluster_pts), float(cluster_pts[:,0].mean())]
            pred = clf.predict([feat])[0]
            if pred == 1:
                human_count += 1
            cluster_feats.append(feat)
        # optional: use regressor to smooth
        if len(cluster_feats) > 0:
            agg = [len(cluster_feats), sum(f[0] for f in cluster_feats), np.mean([f[1] for f in cluster_feats])]
            est = reg.predict([agg])[0]
        else:
            est = 0
        # compute density: area of sector (theta rad). For 180°: theta = pi
        max_r_m = np.nanmax([f[1] for f in cluster_feats]) if cluster_feats else 3.0
        area = 0.5 * (max_r_m**2) * np.pi
        density = human_count / area if area>0 else 0
        print(f"Sweep {sid} -> human_count={human_count} (reg={est:.2f}), density={density:.3f} ppl/m^2")
