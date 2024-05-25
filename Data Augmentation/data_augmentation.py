import os
from PIL import Image
import torchvision.transforms as transforms
import torch
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
import numpy as np

# Define the directory containing the original images
# List of directories to get data from
original_dirs = ['Data/Normal/', 'Data/lesion/' ]

# Define the directory to store the transformed images
transformed_dirs = ['Data/aug_Normal/', 'Data/aug_lesion/' ]

# Define the transformations
transformations = [
    A.Resize(height=320, width=320),
    A.Rotate(limit=60, p=1.0),
    A.HorizontalFlip(p=1.0),
    A.Blur(blur_limit=3),
    A.OpticalDistortion(),
    A.HueSaturationValue(),
    A.VerticalFlip(p=1.0),
    A.CLAHE(clip_limit=2),
    A.RandomBrightnessContrast(),
]
all_transform = A.Compose(transformations)



if __name__ == "__main__":

    # Creating directories if they don't exist
    for directory in transformed_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)

    for original_dir, transformed_dir in zip(original_dirs, transformed_dirs):
        # Iterate over each image in the original directory
        for filename in os.listdir(original_dir):
            # Load the original image
            image_path = os.path.join(original_dir, filename)
            original_image = np.array(Image.open(image_path))

            # Apply each transformation individually and save the resulting images
            for i, transform in enumerate(transformations):
                transformed_image = transform(image=original_image)['image']
                transformed_image = Image.fromarray(transformed_image)
                transformed_filename = f'{os.path.splitext(filename)[0]}_transformed_{i}.jpg'
                transformed_image_path = os.path.join(transformed_dir, transformed_filename)
                transformed_image.save(transformed_image_path)

            all_transformed_image = all_transform(image=original_image)['image']
            all_transformed_image = Image.fromarray(all_transformed_image)
            all_transformed_image_filename = f'{os.path.splitext(filename)[0]}_all_transformed_image_{i}.jpg'
            all_transformed_image_path = os.path.join(transformed_dir, all_transformed_image_filename)
            all_transformed_image.save(all_transformed_image_path)

            print(f'Transformations complete for {filename}')
        print("----------------")