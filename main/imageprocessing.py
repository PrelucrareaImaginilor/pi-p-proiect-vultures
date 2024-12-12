import cv2
import numpy as np
from scipy import ndimage


def preprocess_retinal_image(image):
    # Convertim imaginea la spațiul de culoare LAB pentru a separa mai bine texturile
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Aplicăm CLAHE pe canalul L pentru a îmbunătăți contrastul local
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l)

    # Reducem zgomotul folosind filtre mai sofisticate
    denoised = cv2.bilateralFilter(enhanced_l, 9, 75, 75)

    # Normalizăm imaginea pentru a obține o distribuție uniformă a intensității
    normalized = cv2.normalize(denoised, None, 0, 255, cv2.NORM_MINMAX)

    return normalized


def detect_dark_lesions(preprocessed_image):
    # Aplicăm mai multe tehnici de segmentare
    # 1. Prag adaptiv cu ajustări
    thresh1 = cv2.adaptiveThreshold(
        preprocessed_image, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 15, 3
    )

    # 2. Utilizăm metoda Otsu pentru prag
    _, thresh2 = cv2.threshold(
        preprocessed_image, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Combinăm rezultatele celor două metode
    combined_thresh = cv2.bitwise_and(thresh1, thresh2)

    # Operații morfologice pentru curățare
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened = cv2.morphologyEx(combined_thresh, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)

    # Etichetare componente și filtrare
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(closed, connectivity=8)
    filtered_mask = np.zeros_like(closed)

    # Parametri mai flexibili pentru filtrare
    min_area, max_area = 10, 400
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        eccentricity = stats[label, cv2.CC_STAT_WIDTH] / stats[label, cv2.CC_STAT_HEIGHT]

        if (min_area <= area <= max_area) and (0.5 <= eccentricity <= 2):
            filtered_mask[labels == label] = 255

    return filtered_mask


def detect_bright_lesions(preprocessed_image):
    # Utilizăm tehnici mai avansate de segmentare
    # 1. Prag adaptiv pentru zone luminoase
    _, thresh = cv2.threshold(
        preprocessed_image, 220, 255,
        cv2.THRESH_BINARY
    )

    # Operații morfologice
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    dilated = cv2.dilate(opened, kernel, iterations=1)

    # Etichetare și filtrare componente
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(dilated, connectivity=8)
    filtered_mask = np.zeros_like(dilated)

    # Parametri de filtrare mai detaliat
    min_area, max_area = 20, 600
    for label in range(1, num_labels):
        area = stats[label, cv2.CC_STAT_AREA]
        mean_intensity = np.mean(preprocessed_image[labels == label])
        compactness = (stats[label, cv2.CC_STAT_WIDTH] * stats[label, cv2.CC_STAT_HEIGHT]) / area

        if (min_area <= area <= max_area) and (mean_intensity > 220) and (compactness < 4):
            filtered_mask[labels == label] = 255

    return filtered_mask
