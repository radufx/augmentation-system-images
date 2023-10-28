import os
import cv2

from augmentation import Augmentation


class AugmentationSystem:
    def __init__(self, config_file):
        self.config_file = config_file
        self.augmentations = []
        self.augmentation = Augmentation()

    def read_config(self):
        self.augmentations = []

        with open(self.config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    operation, *params = line.split()
                    self.augmentations.append((operation, params))

    def process_images(self, input_dir, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i, file in enumerate(os.listdir(input_dir)):
            if file.endswith('.jpg'):
                image_path = os.path.join(input_dir, file)
                image = cv2.imread(image_path)

                augmented_images = self.augmentation.apply_augmentations(
                    image, self.augmentations)

                for augmented_image, augmentation in zip(augmented_images, self.augmentations):
                    output_name = os.path.splitext(
                        file)[0] + "_" + augmentation[0]

                    output_path = os.path.join(
                        output_dir, output_name + "_" + str(i+1) + ".jpg")

                    cv2.imwrite(output_path, augmented_image)
