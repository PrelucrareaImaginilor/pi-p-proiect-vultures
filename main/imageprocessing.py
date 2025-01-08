# imageprocessing.py
import os
import cv2
import numpy as np
import tkinter as tk
from diagnosis import generate_diagnosis
from skimage import filters, morphology, measure


class RetinalLesionDetector:
    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

    def preprocess_retinal_image(self, image):
        # Extract green channel (most informative for retinal lesions)
        green_channel = image[:, :, 1]

        # Apply CLAHE for better contrast
        enhanced = self.clahe.apply(green_channel)

        # Bilateral filtering to reduce noise while preserving edges
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Background homogenization
        background = cv2.medianBlur(denoised, 69)
        normalized = cv2.subtract(denoised, background)
        normalized = cv2.normalize(normalized, None, 0, 255, cv2.NORM_MINMAX)

        return normalized

    def detect_dark_lesions(self, preprocessed_image):
        # Adaptive thresholding
        binary = cv2.adaptiveThreshold(
            preprocessed_image,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )

        # Noise removal
        kernel = np.ones((3, 3), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        # Remove small objects and fill holes
        labels = measure.label(cleaned)
        properties = measure.regionprops(labels)

        # Filter based on size and shape
        mask = np.zeros_like(cleaned)
        for prop in properties:
            if prop.area >= 20 and prop.area <= 300 and prop.eccentricity < 0.95:
                coords = prop.coords
                mask[coords[:, 0], coords[:, 1]] = 255

        return mask

    def detect_bright_lesions(self, preprocessed_image):
        # Otsu's thresholding for initial segmentation
        thresh_val = filters.threshold_otsu(preprocessed_image)
        binary = preprocessed_image > (thresh_val * 1.25)  # Higher threshold for bright lesions

        # Morphological operations
        kernel = morphology.disk(2)
        cleaned = morphology.remove_small_objects(binary, min_size=50)
        cleaned = morphology.binary_closing(cleaned, kernel)

        # Convert to uint8
        return (cleaned * 255).astype(np.uint8)

    def analyze_lesions(self, dark_lesions, bright_lesions):
        analysis = {
            'dark_lesion_count': len(measure.regionprops(measure.label(dark_lesions))),
            'bright_lesion_count': len(measure.regionprops(measure.label(bright_lesions))),
            'dark_lesion_area': np.sum(dark_lesions > 0),
            'bright_lesion_area': np.sum(bright_lesions > 0),
            'dark_lesion_density': None,
            'bright_lesion_density': None
        }

        # Calculate lesion density (lesions per unit area)
        total_area = dark_lesions.size
        analysis['dark_lesion_density'] = analysis['dark_lesion_count'] / total_area * 1000
        analysis['bright_lesion_density'] = analysis['bright_lesion_count'] / total_area * 1000

        return analysis


def segment_retinopathy_lesions(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Nu s-a putut citi imaginea.")

    detector = RetinalLesionDetector()
    preprocessed = detector.preprocess_retinal_image(image)
    dark_lesions = detector.detect_dark_lesions(preprocessed)
    bright_lesions = detector.detect_bright_lesions(preprocessed)

    # Analyze detected lesions
    analysis = detector.analyze_lesions(dark_lesions, bright_lesions)

    return image, preprocessed, dark_lesions, bright_lesions, analysis
