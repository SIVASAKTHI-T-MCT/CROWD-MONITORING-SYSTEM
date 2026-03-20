# Working Principle

## 1. Data Acquisition (Firmware)
The Arduino controls the servo motor to sweep from 0° to 180° in fixed steps (e.g., 2°). At each step, the HC-SR04 sends an ultrasonic pulse and measures the time-of-flight to calculate the distance to the nearest object.

Data is streamed over Serial in JSON format:
```json
{"sweep_id": 12, "angle": 45, "distance_cm": 120.5, "ts": 15432}
```

## 2. Spatial Clustering (DBSCAN)
Once a full 180° sweep is completed, the Python backend converts the polar coordinates (angle, distance) into Cartesian (X, Y) coordinates.
DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is used to group adjacent points. This is ideal because we don't know the number of "humans" or "objects" in advance.

## 3. Classification (Random Forest)
Each cluster is characterized by its features:
- Number of points
- Mean distance
- Variance in distance

A pre-trained Random Forest classifier determines if the cluster represents a human based on typical "surface" signatures of a person compared to a wall or furniture.

## 4. Density Calculation
The system calculates the total number of detected humans and divides it by the monitored area (calculated as the area of the 180° sector) to provide a "People per Square Meter" metric.
