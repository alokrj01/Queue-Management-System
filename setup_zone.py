import cv2
import numpy as np
import json 

#Global variables
points = []
config_file = "config.json"

def draw_polygon(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y]) #store click coordinates
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1) #visuals
        
        #connect lines
        if len(points) > 1:
            cv2.line(img, tuple(points[-2]), tuple(points[-1]), (0, 0, 255), 2)
        
        #save json file on 4 points/dots
        if len(points) == 4:
            cv2.line(img, tuple(points[-1]), tuple(points[0]), (0, 0, 255), 2)
            
            # --- main logic ---
            data = {
                "camera_source": 0,       # Webcam ID (can be changed by Client)
                "zone_coordinates": points, # Clicked points
                "max_wait_threshold": 60  # Example:send alerts if 60 sec exceeds (future use)
            }

            with open(config_file, "w") as f:
                json.dump(data, f, indent=4)
            
            print(f"\n[SUCCESS] Settings saved to {config_file}")
            print(f"Coordinates: {points}")
            print("Now, run main.py.\n")

#camera start
cap = cv2.VideoCapture(0)

cv2.namedWindow("Setup Zone")
cv2.setMouseCallback("Setup Zone", draw_polygon)

print("--- ADMIN MODE ---")
print("Click 4 points to set the Queue Zone.")
print("Press 'r' to Reset, 'q' to Quit.")

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.resize(frame, (1020, 720))
    img = frame.copy()

    #Draw existing points
    if len(points) > 0:
        for i in range(len(points)):
            cv2.circle(img, tuple(points[i]), 5, (0, 0, 255), -1)
            if i > 0:
                cv2.line(img, tuple(points[i-1]), tuple(points[i]), (0, 0, 255), 2)
        if len(points) == 4:
            cv2.line(img, tuple(points[3]), tuple(points[0]), (0, 0, 255), 2)
            #fill area
            pts = np.array(points, np.int32)
            cv2.fillPoly(img, [pts], (0, 255, 0, 100))

    cv2.imshow("Setup Zone", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        points = [] # Reset
        print("Reset done.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()