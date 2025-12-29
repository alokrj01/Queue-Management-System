import cv2
import numpy as np
import time
import json
import os
from ultralytics import YOLO

# Queue Zone (set Coordinates a/c to camera)
def load_zone_config():
    config_file = "config.json"
    
    # Default settings
    default_config = {
        "camera_source": 0,
        "zone_coordinates": [[0, 0], [1020, 0], [1020, 720], [0, 720]]
    }

    if not os.path.exists(config_file):
        print("[WARNING] Didn't get Config file. Using Default settings.")
        return default_config
    
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            print("[INFO] Config loaded successfully!")
            return config
    except Exception as e:
        print(f"[ERROR] JSON file corrupt hai: {e}")
        return default_config

def run_queue_logic(source=0, conf=0.3):    

  #Load Config
  config = load_zone_config()

  #Extract Data
  camera_source = source if source is not None else config.get("camera_source", 0)
  zone_coords = config.get("zone_coordinates")
  queue_zone = np.array(zone_coords, np.int32) # convert into Numpy array

  #System Start
  model = YOLO('yolov8n.pt') 
  cap = cv2.VideoCapture(camera_source)
  people_timers = {}

  while True:
      ret, frame = cap.read()
      if not ret: break
      frame = cv2.resize(frame, (1020, 720))

      # --- TRACKING ---
      results = model.track(frame, classes=[0], persist=True, conf=0.3, verbose=False)
      
      current_time = time.time()
      current_ids_in_zone = []
      queue_count = 0

      if results[0].boxes.id is not None:
          boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
          track_ids = results[0].boxes.id.cpu().numpy().astype(int)

          for box, track_id in zip(boxes, track_ids):
              x1, y1, x2, y2 = box
              feet_x, feet_y = int((x1 + x2) / 2), int(y2)

              #CHECK ZONE (Loaded from JSON)
              is_inside = cv2.pointPolygonTest(queue_zone, (feet_x, feet_y), False)

              if is_inside >= 0:
                  queue_count += 1
                  current_ids_in_zone.append(track_id)
                  if track_id not in people_timers:
                      people_timers[track_id] = current_time
                  
                  elapsed = int(current_time - people_timers[track_id])
                  
                  cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                  cv2.putText(frame, f"{elapsed}s", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
              else:
                  cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

      # Cleanup
      for pid in list(people_timers.keys()):
          if pid not in current_ids_in_zone:
              del people_timers[pid]

      # Visuals
      cv2.polylines(frame, [queue_zone], True, (255, 255, 0), 2)
      
      # Stats
      if people_timers:
          avg = int(sum([current_time - t for t in people_timers.values()]) / len(people_timers))
      else:
          avg = 0
          
      cv2.rectangle(frame, (20, 20), (350, 100), (0, 0, 0), -1)
      cv2.putText(frame, f"Count: {queue_count}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
      cv2.putText(frame, f"Avg Time: {avg}s", (30, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

      cv2.imshow("Queue System", frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break

  cap.release()

if __name__ == "__main__":
    for frame, stats in run_queue_logic():
        cv2.imshow("Main Logic Test", frame)
        if cv2.waitKey(1) == ord('q'):
            break
        
cv2.destroyAllWindows()