import cv2
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt


def preprocess_retinal_image(image):
    """
    Preprocess retinal image for lesion segmentation.

    Args:
        image (numpy.ndarray): Input retinal image in BGR format

    Returns:
        numpy.ndarray: Preprocessed image
    """
    # Convert to green channel (best contrast for retinal features)
    green_channel = image[:, :, 1]

    # Apply CLAHE for contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_enhanced = clahe.apply(green_channel)

    # Denoise image
    denoised = cv2.medianBlur(contrast_enhanced, 5)

    # Normalize image
    normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)

    return normalized


def detect_dark_lesions(preprocessed_image):
    """
    Detect dark lesions (microaneurysms and hemorrhages).

    Args:
        preprocessed_image (numpy.ndarray): Preprocessed retinal image

    Returns:
        numpy.ndarray: Binary mask of detected dark lesions
    """
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        preprocessed_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2
    )

    # Remove small noise
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Fill holes
    filled = ndimage.binary_fill_holes(opened).astype(np.uint8) * 255

    # Remove large connected components (likely blood vessels)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        filled, connectivity=8
    )

    # Filter based on area
    min_area = 5  # minimum area for lesion
    max_area = 300  # maximum area for lesion
    filtered_mask = np.zeros_like(filled)

    for label in range(1, num_labels):  # Skip background (label 0)
        area = stats[label, cv2.CC_STAT_AREA]
        if min_area <= area <= max_area:
            filtered_mask[labels == label] = 255

    return filtered_mask


def detect_bright_lesions(preprocessed_image):
    """
    Detect bright lesions (exudates).

    Args:
        preprocessed_image (numpy.ndarray): Preprocessed retinal image

    Returns:
        numpy.ndarray: Binary mask of detected bright lesions
    """
    # Apply Otsu's thresholding
    _, thresh = cv2.threshold(
        preprocessed_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Remove small noise
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # Remove large connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        opened, connectivity=8
    )

    # Filter based on area and intensity
    min_area = 10  # minimum area for exudate
    max_area = 500  # maximum area for exudate
    filtered_mask = np.zeros_like(opened)

    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        component = (labels == label)
        mean_intensity = np.mean(preprocessed_image[component])

        if min_area <= area <= max_area and mean_intensity > 200:
            filtered_mask[component] = 255

    return filtered_mask


def segment_retinopathy_lesions(image_path):
    """
    Main function to segment both dark and bright lesions in retinal image.

    Args:
        image_path (str): Path to input retinal image

    Returns:
        tuple: (dark_lesion_mask, bright_lesion_mask)
    """
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read image from path")

    # Preprocess image
    preprocessed = preprocess_retinal_image(image)

    # Detect lesions
    dark_lesions = detect_dark_lesions(preprocessed)
    bright_lesions = detect_bright_lesions(preprocessed)

    return dark_lesions, bright_lesions


def visualize_results(image_path, dark_mask, bright_mask):
    """
    Visualize original image with detected lesions overlaid.

    Args:
        image_path (str): Path to original image
        dark_mask (numpy.ndarray): Binary mask of dark lesions
        bright_mask (numpy.ndarray): Binary mask of bright lesions
    """
    # Read original image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create overlay
    overlay = image.copy()
    overlay[dark_mask == 255] = [255, 0, 0]  # Red for dark lesions
    overlay[bright_mask == 255] = [0, 255, 0]  # Green for bright lesions

    # Display results
    plt.figure(figsize=(15, 5))

    plt.subplot(131)
    plt.imshow(image)
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(132)
    plt.imshow(dark_mask, cmap='gray')
    plt.title('Dark Lesions')
    plt.axis('off')

    plt.subplot(133)
    plt.imshow(bright_mask, cmap='gray')
    plt.title('Bright Lesions')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


# Example usage
if __name__ == "__main__":
    image_path = "IMG/bg1.png"
    image_path2= "IMG/bg2.png"
    try:
        dark_lesions, bright_lesions = segment_retinopathy_lesions(image_path)
        visualize_results(image_path, dark_lesions, bright_lesions)

        dark_lesions, bright_lesions = segment_retinopathy_lesions(image_path2)
        visualize_results(image_path2, dark_lesions, bright_lesions)
    except Exception as e:
        print(f"Error processing image: {str(e)}")