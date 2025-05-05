# Auto-Video-Trimmer-for-endoscopy-operations-using-opencv-and-python

Smart Endoscopy Video Trimmer using OpenCV

This Python-based tool automatically scans and processes endoscopy videos to extract only the meaningful clips—segments containing medical-grade visuals (e.g., stainless steel tools or active scenes)—while skipping blurry, black, or idle footage.

Key Features
	•	Automatic Trimming: Cuts and saves only the relevant parts of long endoscopy videos.
	•	Steel Detection: Uses HSV-based color filtering to detect presence of stainless steel tools in the frame.
	•	Chunk-Based Processing: Processes video in 10-second windows (4 sec active, 6 sec skip) for fast and efficient analysis.
	•	Multi-Drive Workflow: Scans input videos from one drive (e.g., external HDD) and saves processed clips to another (e.g., SSD or backup drive).
	•	Batch Processing: Handles thousands of videos in nested folders using os.walk.

Technologies Used
	•	Python 3
	•	OpenCV (cv2)
	•	NumPy
	•	JSON (for logging processed files)
	•	Compatible with .mp4, .avi, .mov, .mkv, and other common formats

How It Works
	1.	Load a video and divide it into time blocks.
	2.	Analyze each block using frame-by-frame steel detection.
	3.	If majority of frames in the block contain medical tool indicators (like steel), the chunk is saved.
	4.	The script skips redundant or idle segments to generate a concise, medically useful video.

Use Case

Ideal for medical institutions, doctors, and researchers looking to:
	•	Reduce storage space.
	•	Focus on diagnostically relevant content.
	•	Automate preprocessing of endoscopy archives.
