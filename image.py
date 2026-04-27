"""
Image Processing Algorithms
Algorithms: 1. Grayscale Conversion, 2. Edge Detection (Canny)
"""

import cv2
import numpy as np
import os

#create an output directory
def ensure_output_dir():
    if not os.path.exists('output'):
        os.makedirs('output')

def grayscale_conversion(image_path):
    """
    Algorithm 1: Convert RGB image to grayscale
    Principle: Weighted sum of Red, Green, Blue channels based on human perception
    Formula: Gray = 0.299*R + 0.587*G + 0.114*B
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return None, "Error: Could not load image"
    
    # Method 1: Using OpenCV (for demonstration)
    gray_cv2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Method 2: Manual implementation (to show the formula)
    height, width = img.shape[:2]
    gray_manual = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            b, g, r = img[i, j]  # OpenCV uses BGR order
            # The formula: Gray = 0.299*R + 0.587*G + 0.114*B
            gray_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_manual[i, j] = gray_value
    
    # Save result
    ensure_output_dir()
    output_path = 'output/grayscale_output.jpg'
    cv2.imwrite(output_path, gray_cv2)
    
    return gray_cv2, f"Grayscale conversion complete. Saved to {output_path}"

#Algorithm 2: Edge detection using Canny algorithm
def edge_detection(image_path):
    
    # Read image as grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None, "Error: Could not load image"
    
    # Apply Gaussian blur to reduce noise (standard preprocessing for Canny)
    blurred = cv2.GaussianBlur(img, (5, 5), 1.4)
    
    # Canny edge detection
    # Parameters: image, threshold1, threshold2
    # Lower threshold = 50, Upper threshold = 150
    edges = cv2.Canny(blurred, 50, 150)
    
    # Manual Sobel calculation (to show the mathematical principle)
    # Sobel X kernel
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    # Sobel Y kernel
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    # Calculate gradients (for demonstration)
    grad_x = cv2.filter2D(img.astype(np.float32), -1, sobel_x)
    grad_y = cv2.filter2D(img.astype(np.float32), -1, sobel_y)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    grad_magnitude = np.uint8(np.clip(grad_magnitude, 0, 255))
    
    # Save result
    ensure_output_dir()
    output_path = 'output/edge_output.jpg'
    cv2.imwrite(output_path, edges)
    
    explanation = (f"Edge detection complete. Using Canny algorithm with thresholds 50 and 150.\n"
                   f"Mathematical principle: Gradient magnitude = √(Gx² + Gy²)\n"
                   f"Where Gx and Gy are Sobel operator convolutions.\n"
                   f"Saved to {output_path}")
    
    return edges, explanation

# Test functions (run this file directly to test)
if __name__ == "__main__":
    print("Image Algorithms Module")
    print("-" * 30)
    print("Functions available:")
    print("1. grayscale_conversion(image_path)")
    print("2. edge_detection(image_path)")