#Frame Extraction

import cv2
import numpy as np
import os

def ensure_output_dir():
    """Create output directories if they don't exist"""
    if not os.path.exists('output'):
        os.makedirs('output')
    if not os.path.exists('output/frames'):
        os.makedirs('output/frames')

def extract_frames(video_path, frame_interval=30):
    """
    Algorithm 3: Extract frames from video
    Principle: Read video file sequentially and save individual frames as images
    Formula: Frame position = frame_index / fps (time in seconds)
    """
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Error: Could not open video file"
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    ensure_output_dir()
    frames_dir = 'output/frames'
    
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save every Nth frame
        if frame_count % frame_interval == 0:
            output_path = f'{frames_dir}/frame_{saved_count:04d}.jpg'
            cv2.imwrite(output_path, frame)
            saved_count += 1
        
        frame_count += 1
    
    cap.release()
    
    result_msg = (f"Frame extraction complete.\n"
                  f"Total frames in video: {total_frames}\n"
                  f"Extracted {saved_count} frames (every {frame_interval} frames)\n"
                  f"Saved to {frames_dir}/")
    
    return saved_count, result_msg

#Motion Detection (Frame Differencing) Algorithm
def motion_detection(video_path):
    """
    Algorithm 4: Motion detection using frame differencing
    Principle: Compute absolute difference between consecutive frames
    Formula: |frame_t - frame_{t-1}| > threshold → motion detected
    """
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None, "Error: Could not open video file"
    
    ensure_output_dir()
    output_path = 'output/motion_output.avi'
    
    # Get video properties for output
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define codec and create VideoWriter for output
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Read first frame
    ret, prev_frame = cap.read()
    if not ret:
        return None, "Error: Could not read video"
    
    # Convert to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    motion_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert current frame to grayscale
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate absolute difference between frames
        # Formula: diff = |current_frame - previous_frame|
        diff = cv2.absdiff(curr_gray, prev_gray)
        
        # Apply threshold to highlight motion
        # Formula: motion_mask = 255 if diff > threshold else 0
        threshold = 30  # Sensitivity threshold
        _, motion_mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Find contours of motion areas
        contours, _ = cv2.findContours(motion_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw rectangles around motion areas
        motion_frame = frame.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Ignore small movements (noise)
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(motion_frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                motion_count += 1
        
        # Add text showing motion status
        if len(contours) > 0:
            cv2.putText(motion_frame, "MOTION DETECTED", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(motion_frame, "No Motion", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Write frame to output video
        out.write(motion_frame)
        
        # Update previous frame
        prev_gray = curr_gray
    
    # Release everything
    cap.release()
    out.release()
    
    result_msg = (f"Motion detection complete.\n"
                  f"Mathematical principle: Motion = |F(t) - F(t-1)| > threshold\n"
                  f"Threshold used: {threshold}\n"
                  f"Detected motion in multiple frames.\n"
                  f"Output saved to {output_path}")
    
    return output_path, result_msg

# Test functions
if __name__ == "__main__":
    print("Video Algorithms Module")
    print("-" * 30)
    print("Functions available:")
    print("1. extract_frames(video_path, frame_interval=30)")
    print("2. motion_detection(video_path)")