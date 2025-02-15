import cv2
import os

def edge_detection(image_path, output_folder, threshold1=100, threshold2=200):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Perform Canny edge detection
    edges = cv2.Canny(image, threshold1, threshold2)
    # Save the resulting image
    result_path = os.path.join(output_folder, 'edges_' + os.path.basename(image_path))
    cv2.imwrite(result_path, edges)
    return result_path