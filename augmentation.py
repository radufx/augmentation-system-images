import cv2
import numpy as np


class Augmentation:
    def __init__(self):
        pass

    # geometric transformations
    def rotate_image(self, image, angle):
        rows, cols, _ = image.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
        return cv2.warpAffine(image, M, (cols, rows))

    def resize_image(self, image, scale_percent):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

    def flip_image(self, image, mode):
        if mode == 'horizontal':
            return image[:, ::-1, :]
        elif mode == 'vertical':
            return image[::-1, :, :]
        else:
            return image

    # low-level translation
    def translate_image(self, image, offset_x, offset_y):
        rows, cols, _ = image.shape
        translated_image = np.zeros(image.shape, dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                if 0 <= i + offset_y < rows and 0 <= j + offset_x < cols:
                    translated_image[i + offset_y, j + offset_x] = image[i, j]
        return translated_image

    def pixelate_image(self, image, block_size):
        h, w, _ = image.shape
        return cv2.resize(cv2.resize(image, (w // block_size, h // block_size), interpolation=cv2.INTER_NEAREST), (w, h), interpolation=cv2.INTER_NEAREST)

    def increase_brightness(self, image, value):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        return cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    # Filtering augmentation functions
    def sharpen_image(self, image):
        kernel = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)

    # low-level grayscale manipulation
    def apply_grayscale(self, image):
        image_copy = image.copy()
        height, width, _ = image.shape
        for i in range(height):
            for j in range(width):
                pixel = image[i, j]
                gray_value = int(
                    0.3 * pixel[2] + 0.59 * pixel[1] + 0.11 * pixel[0])
                image_copy[i, j] = [gray_value, gray_value, gray_value]
        return image_copy

    # Function to apply augmentation algorithms
    def apply_augmentations(self, image, augmentations):
        images = []

        for augmentation in augmentations:
            operation, params = augmentation

            if operation == "rotate":
                images.append(self.rotate_image(image, int(params[0])))
            elif operation == "translate":
                images.append(self.translate_image(
                    image, int(params[0]), int(params[1])))
            elif operation == "resize":
                images.append(self.resize_image(image, int(params[0])))
            elif operation == "flip":
                images.append(self.flip_image(image, params[0]))
            elif operation == "pixelate":
                images.append(self.pixelate_image(image, int(params[0])))
            elif operation == "increase_brightness":
                images.append(self.increase_brightness(image, int(params[0])))
            elif operation == "sharpen":
                images.append(self.sharpen_image(image))
            elif operation == "grayscale":
                images.append(self.apply_grayscale(image))

        return images
