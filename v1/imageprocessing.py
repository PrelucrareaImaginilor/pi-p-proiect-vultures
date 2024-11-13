import cv2
import numpy as np
from scipy import ndimage


# Metoda care îmbunătățește contrastul imaginii
def preprocess_retinal_image(image):
    green_channel = image[:, :, 1]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(green_channel)
    denoised = cv2.medianBlur(contrast_enhanced, 5)
    normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)
    return normalized


# Metoda pentru detectarea leziunilor întunecate (microanevrismele și hemoragiile)
def detect_dark_lesions(preprocessed_image):
    thresh = cv2.adaptiveThreshold(
        preprocessed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    filled = ndimage.binary_fill_holes(opened).astype(np.uint8) * 255
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(filled, connectivity=8)
    filtered_mask = np.zeros_like(filled)
    min_area, max_area = 5, 300
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        if min_area <= area <= max_area:
            filtered_mask[labels == label] = 255
    return filtered_mask


# Metoda pentru detectarea leziunilor luminoase (exudatele)
def detect_bright_lesions(preprocessed_image):
    _, thresh = cv2.threshold(
        preprocessed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(opened, connectivity=8)
    filtered_mask = np.zeros_like(opened)
    min_area, max_area = 10, 500
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        mean_intensity = np.mean(preprocessed_image[labels == label])
        if min_area <= area <= max_area and mean_intensity > 200:
            filtered_mask[labels == label] = 255
    return filtered_mask
