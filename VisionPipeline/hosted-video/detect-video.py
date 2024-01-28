import subprocess
import time
import imageio
import numpy as np
import cv2
import json

# Specify the path to store the recorded video clip
recorded_video_path = "validation-videos/recorded_clip.mp4"

# Execute the terminal command to record a 30-second video clip
record_command = ["nvgstcapture-1.0", "--orientation=2", "--video-res=2", "--mode=2", "--automate", "--capture-auto", "--capture-time=30"]
with open(recorded_video_path, "wb") as output_file:
    subprocess.run(record_command, stdout=output_file, stderr=subprocess.PIPE)

# Wait for a short time to ensure the recording is completed
time.sleep(2)

# Load the recorded video clip
cap = cv2.VideoCapture(recorded_video_path)

# Get the video information
width = int(cap.get(3))
height = int(cap.get(4))
fps = int(cap.get(5))

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video_path = "output_videos/comp_test_with_boxes.mp4"
writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# Ensure the writer is successfully initialized
if not writer.isOpened():
    print("Error: Video writer not successfully opened.")
    exit()

# Process each frame and draw bounding boxes
while True:
    ret, frame_np = cap.read()
    if not ret:
        break

    # Process each frame and draw bounding boxes
    for frame_number, frame_info in enumerate(results.get('frames', [])):
        if not isinstance(frame_info, dict):
            print(f"Skipping frame {frame_number + 1} due to unexpected format. Frame content: {frame_info}")
            continue

        frame = frame_info.get('data', {})
        if not isinstance(frame, dict) or 'objects' not in frame:
            print(f"Skipping frame {frame_number + 1} because it does not contain 'objects'. Frame content: {frame}")
            continue

        # Ensure the frame data is in the correct format
        frame_np = np.array(frame['image'], dtype=np.uint8)

        for prediction in frame['objects']:
            bbox = prediction.get('bbox', {})
            label = prediction.get('label', '')
            confidence = prediction.get('confidence', 0.0)

            # Draw bounding box on the frame
            cv2.rectangle(frame_np, (int(bbox.get('xmin', 0)), int(bbox.get('ymin', 0))),
                        (int(bbox.get('xmax', 0)), int(bbox.get('ymax', 0))), (0, 255, 0), 2)
            cv2.putText(frame_np, f"{label}: {confidence:.2f}", (int(bbox.get('xmin', 0)), int(bbox.get('ymin', 0)) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Write the frame with bounding boxes to the output video
    writer.write(frame_np)

cap.release()
writer.release()

print(f"Video with bounding boxes saved at: {output_video_path}")