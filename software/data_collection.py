# serial_collector.py
import serial, json, time, os
from collections import defaultdict

SERIAL_PORT = "/dev/ttyUSB0"   # change as needed
BAUD = 115200
OUT_DIR = "data/raw"
os.makedirs(OUT_DIR, exist_ok=True)

def run():
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    print("Listening on", SERIAL_PORT)
    current_sweep = None
    sweeps = {}
    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception as e:
                print("bad json:", line[:200])
                continue
            sid = obj.get("sweep_id")
            angle = obj.get("angle")
            d = obj.get("distance_cm")
            ts = obj.get("ts", int(time.time()*1000))
            if sid is None:
                continue
            if sid not in sweeps:
                # start new sweep accumulator
                sweeps[sid] = {"sweep_id": sid, "ts": ts, "angles": [], "distances": []}
            sweeps[sid]["angles"].append(angle)
            sweeps[sid]["distances"].append(d)
            # Heuristic: when we have an angle == 180 or angle decreased, we can flush
            if angle == 180 or (len(sweeps[sid]["angles"]) > 1 and sweeps[sid]["angles"][-1] < sweeps[sid]["angles"][-2]):
                # save sweep to file (append)
                fname = os.path.join(OUT_DIR, f"sweep_{sid}_{int(time.time())}.json")
                with open(fname, "w") as f:
                    json.dump(sweeps[sid], f)
                print("Saved", fname)
                del sweeps[sid]
    except KeyboardInterrupt:
        print("Stopping.")
    finally:
        ser.close()

if __name__ == "__main__":
    run()
