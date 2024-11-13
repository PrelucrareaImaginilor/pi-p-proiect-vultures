import cv2
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def calculate_metrics(predicted_mask, ground_truth_mask):
    """
    Calculate evaluation metrics for segmentation results.

    Args:
        predicted_mask (numpy.ndarray): Binary mask of predicted lesions
        ground_truth_mask (numpy.ndarray): Binary mask of ground truth lesions

    Returns:
        dict: Dictionary containing evaluation metrics
    """
    # Flatten masks for metric calculation
    y_pred = predicted_mask.ravel()
    y_true = ground_truth_mask.ravel()

    # Calculate metrics
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0)
    }

    # Calculate Dice coefficient
    intersection = np.sum(predicted_mask * ground_truth_mask)
    dice = (2. * intersection) / (np.sum(predicted_mask) + np.sum(ground_truth_mask))
    metrics['dice'] = dice

    return metrics


def plot_confusion_matrix(predicted_mask, ground_truth_mask):
    """
    Plot confusion matrix for segmentation results.

    Args:
        predicted_mask (numpy.ndarray): Binary mask of predicted lesions
        ground_truth_mask (numpy.ndarray): Binary mask of ground truth lesions
    """
    cm = confusion_matrix(ground_truth_mask.ravel(), predicted_mask.ravel())

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('Ground Truth')
    plt.xlabel('Predicted')
    plt.show()


def evaluate_dataset(segmentation_func, image_paths, ground_truth_paths):
    """
    Evaluate segmentation results on entire dataset.

    Args:
        segmentation_func: Function that performs segmentation
        image_paths (list): List of paths to retinal images
        ground_truth_paths (list): List of paths to ground truth masks

    Returns:
        dict: Average metrics across dataset
    """
    all_metrics = []

    for img_path, gt_path in zip(image_paths, ground_truth_paths):
        # Perform segmentation
        dark_mask, bright_mask = segmentation_func(img_path)
        combined_mask = np.logical_or(dark_mask, bright_mask).astype(np.uint8)

        # Load ground truth
        ground_truth = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
        ground_truth = (ground_truth > 0).astype(np.uint8)

        # Calculate metrics
        metrics = calculate_metrics(combined_mask, ground_truth)
        all_metrics.append(metrics)

    # Calculate average metrics
    avg_metrics = {}
    for metric in all_metrics[0].keys():
        avg_metrics[metric] = np.mean([m[metric] for m in all_metrics])

    return avg_metrics


def plot_roc_curve(predicted_probs, ground_truth):
    """
    Plot ROC curve for segmentation results.

    Args:
        predicted_probs (numpy.ndarray): Probability predictions for each pixel
        ground_truth (numpy.ndarray): Binary ground truth mask
    """
    from sklearn.metrics import roc_curve, auc

    fpr, tpr, _ = roc_curve(ground_truth.ravel(), predicted_probs.ravel())
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()