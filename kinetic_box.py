import cv2
import numpy as np
import random
import math
import os

# === CONFIGURATION ===
VIDEO_PATH = 'your_video.mp4'  # Replace with your actual video file
OUTPUT_FILENAME = 'output_with_hitboxes.mp4'
MAX_HITBOXES_IN_REGION = 3
PROXIMITY_THRESHOLD = 100  # pixels
MAX_MATCH_DISTANCE = 50     # pixels
    
# === SETUP ===
cap = cv2.VideoCapture(VIDEO_PATH)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILENAME, fourcc, fps, (width, height))

fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
tracked_objects = {}  # object_id: {'centroid': (x, y), 'color': (b, g, r), 'last_seen': frame_count}
next_object_id = 0
frame_count = 0


def get_random_color():
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Red, Green, Blue
    return random.choice(colors)


def count_nearby(centroid, centroids_list, threshold):
    count = 0
    for c in centroids_list:
        if math.hypot(c[0] - centroid[0], c[1] - centroid[1]) < threshold:
            count += 1
    return count


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    fgmask = fgbg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    drawn_centroids = []
    updated_objects = {}

    for cnt in contours:
        if cv2.contourArea(cnt) < 500:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2
        centroid = (cx, cy)

        # Skip if too many hitboxes already in this region
        if count_nearby(centroid, drawn_centroids, PROXIMITY_THRESHOLD) >= MAX_HITBOXES_IN_REGION:
            continue

        # Try to match with existing tracked objects
        matched_id = None
        for obj_id, data in tracked_objects.items():
            prev_cx, prev_cy = data['centroid']
            distance = math.hypot(prev_cx - cx, prev_cy - cy)
            if distance < MAX_MATCH_DISTANCE:
                matched_id = obj_id
                break

        if matched_id is None:
            matched_id = next_object_id
            tracked_objects[matched_id] = {
                'centroid': centroid,
                'color': get_random_color(),
                'last_seen': frame_count
            }
            next_object_id += 1
            speed = 0
        else:
            prev_cx, prev_cy = tracked_objects[matched_id]['centroid']
            speed = math.hypot(prev_cx - cx, prev_cy - cy)
            tracked_objects[matched_id]['centroid'] = centroid
            tracked_objects[matched_id]['last_seen'] = frame_count

        # Draw hitbox and speed text
        color = tracked_objects[matched_id]['color']
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{speed:.2f} px/frame", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        drawn_centroids.append(centroid)
        updated_objects[matched_id] = tracked_objects[matched_id]

    # Clean up objects not seen for a while (optional)
    inactive_ids = [obj_id for obj_id, data in tracked_objects.items()
                    if frame_count - data['last_seen'] > 30]
    for obj_id in inactive_ids:
        del tracked_objects[obj_id]

    out.write(frame)

cap.release()
out.release()
cv2.destroyAllWindows()

print(f"\n✅ Processing complete! Video saved as: {os.path.abspath(OUTPUT_FILENAME)}")
