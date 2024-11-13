import os
import cv2
import numpy as np
import tkinter as tk
from imageprocessing import preprocess_retinal_image, detect_dark_lesions, detect_bright_lesions
from diagnosis import generate_diagnosis


def segment_retinopathy_lesions(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Nu s-a putut citi imaginea.")
    preprocessed = preprocess_retinal_image(image)
    dark_lesions = detect_dark_lesions(preprocessed)
    bright_lesions = detect_bright_lesions(preprocessed)
    return image, preprocessed, dark_lesions, bright_lesions


def create_image_with_title(image, title, border_size=10):
    color = [255, 255, 255]
    image_with_border = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size,
                                           cv2.BORDER_CONSTANT, value=color)
    title_height = 30
    title_image = np.full((title_height, image_with_border.shape[1], 3), 255, dtype=np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color_text = (0, 0, 0)
    thickness = 1
    text_size = cv2.getTextSize(title, font, font_scale, thickness)[0]
    text_x = (title_image.shape[1] - text_size[0]) // 2
    text_y = (title_image.shape[0] + text_size[1]) // 2
    cv2.putText(title_image, title, (text_x, text_y), font, font_scale, color_text, thickness)

    return cv2.vconcat([title_image, image_with_border])


def show_images_grid(original, preprocessed, dark_lesions, bright_lesions):
    preprocessed = cv2.cvtColor(preprocessed, cv2.COLOR_GRAY2BGR)
    dark_lesions = cv2.cvtColor(dark_lesions, cv2.COLOR_GRAY2BGR)
    bright_lesions = cv2.cvtColor(bright_lesions, cv2.COLOR_GRAY2BGR)

    original_with_title = create_image_with_title(original, "Original")
    preprocessed_with_title = create_image_with_title(preprocessed, "Rezultatul procesarii")
    dark_lesions_with_title = create_image_with_title(dark_lesions, "Leziunile intunecate")
    bright_lesions_with_title = create_image_with_title(bright_lesions, "Leziunile luminoase")

    top_row = cv2.hconcat([original_with_title, preprocessed_with_title])
    bottom_row = cv2.hconcat([dark_lesions_with_title, bright_lesions_with_title])
    grid_image = cv2.vconcat([top_row, bottom_row])

    cv2.imshow("Segmentarea leziunilor", grid_image)

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    window_width = grid_image.shape[1]
    window_height = grid_image.shape[0]
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    cv2.moveWindow("Segmentarea leziunilor", x, y)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    os.makedirs("diagnosis", exist_ok=True)
    image_files = [f for f in os.listdir("dataset") if f.endswith('.jpg') or f.endswith('.png')]
    if not image_files:
        print("Nu au fost găsite imagini!")
    else:
        for image_file in image_files:
            image_path = f"dataset/{image_file}"
            original, preprocessed_image, dark_lesions, bright_lesions = segment_retinopathy_lesions(image_path)
            filename = os.path.splitext(image_file)[0]

            generate_diagnosis(dark_lesions | bright_lesions, filename)
            show_images_grid(original, preprocessed_image, dark_lesions, bright_lesions)
