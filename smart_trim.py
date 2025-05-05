import os
import cv2
import numpy as np
import json

# Configurable Paths
SOURCE_ROOT = "/Volumes/WD BLANK"  # Input drive
DEST_ROOT = "/Volumes/T7/WD_BLANK_STRUCTURE"  # Output drive
LOG_FILE = os.path.join(DEST_ROOT, "processed_videos.json")

# Load or initialize processed log
if os.path.exists(LOG_FILE):
    try:
        with open(LOG_FILE, "r") as f:
            processed = set(json.load(f))
    except json.decoder.JSONDecodeError:
        print("⚠️ Error reading the JSON log. Initializing a new log.")
        processed = set()
else:
    processed = set()

def contains_steel(frame, gray_thresh=60, saturation_thresh=50):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    _, s, v = cv2.split(hsv)
    steel_mask = (s < saturation_thresh) & (v > gray_thresh)
    return (np.count_nonzero(steel_mask) / frame.size) > 0.05  # 5% of frame is likely steel

def clip_contains_steel(cap, start_frame, fps, duration_sec=4):
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frames_to_check = int(duration_sec * fps)
    detected = 0
    for _ in range(frames_to_check):
        ret, frame = cap.read()
        if not ret:
            break
        if contains_steel(frame):
            detected += 1
    return detected > frames_to_check // 2  # Majority frames show steel

def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"❌ Failed to open video: {input_path}")
        return False

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Use 'mp4v' codec for MP4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_num = 0
    chunk = 0

    while frame_num < total:
        print(f"🔍 Checking chunk {chunk} starting at {frame_num // fps} sec...")

        if clip_contains_steel(cap, frame_num, fps):
            print("✅ Steel detected. Including this 4-sec clip.")
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            for _ in range(4 * fps):  # Adjust the 4-sec chunk length if needed
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
        else:
            print("❌ No steel detected. Skipping this clip.")

        frame_num += (4 + 6) * fps  # Move to next 4+6 sec block (can adjust to increase chunk size)
        chunk += 1

    cap.release()
    out.release()
    return True

# List of video formats to process
video_formats = (
    '.3gp', '.avi', '.flv', '.mkv', '.mov', '.mp4', '.mpg', '.vob', '.webm', '.wmv'
)

# Process all videos
videos_processed = 0

for root, _, files in os.walk(SOURCE_ROOT):
    for file in files:
        if not file.lower().endswith(video_formats):
            continue

        full_input = os.path.join(root, file)
        rel_path = os.path.relpath(full_input, SOURCE_ROOT)
        
        # Skip already processed files
        if rel_path in processed:
            continue

        # Create full output path for each video
        full_output = os.path.join(DEST_ROOT, rel_path)
        
        # Ensure destination directory exists
        dest_dir = os.path.dirname(full_output)
        os.makedirs(dest_dir, exist_ok=True)

        # Add the .mp4 extension if it's not already present
        if not full_output.lower().endswith('.mp4'):
            full_output += '.mp4'

        print(f"Processing video: {full_input} -> Saving to: {full_output}")

        if process_video(full_input, full_output):
            processed.add(rel_path)
            videos_processed += 1
            with open(LOG_FILE, "w") as f:
                json.dump(list(processed), f)

print(f"✅ {videos_processed} videos processed and saved successfully.")
