# -------------------------------------------------------------------------------------
#  Originally Developed by :  Ignitarium Technology Solutions Pvt. Ltd.
#  This file is released under permissive terms. You may use,
#  modify, copy or distribute this file without restriction as long as this
#  section of the header (“Originally Developed by”) is retained
#  without modification.
# -------------------------------------------------------------------------------------
#  Filename    : fine_tune.py
# -------------------------------------------------------------------------------------
#  Description : SAM segmentation finetune code
# -------------------------------------------------------------------------------------

import torch
import shutil
import os
import numpy as np
from torch.utils.data import Dataset as dt
from torch.utils.data import DataLoader
from transformers import SamModel
from transformers import SamProcessor

import monai
from tqdm import tqdm
from statistics import mean
import torch.nn.functional as F
import json
import time
from datasets import Dataset
import matplotlib.pyplot as plt
from torch.optim import Adam
from PIL import Image, ImageDraw
import cv2
import argparse

def load_contours_from_json(json_file):
    contours = []
    img_full_path = None

    with open(json_file) as f:
        json_data = json.load(f)
        image_path = json_data['imagePath']
        img_full_path = os.path.join(os.path.dirname(json_file), image_path)

        for shape in json_data['shapes']:
            if shape['shape_type'] == 'polygon':
                contour_points = shape['points']
                contours.append(contour_points)

    return contours, img_full_path

def get_bounding_box(ground_truth_map):
    try:
        # get bounding box from mask
        y_indices, x_indices = np.where((ground_truth_map > 0))
        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)
        H, W = ground_truth_map.shape
        x_min = max(0, x_min - np.random.randint(0, 20))
        x_max = min(W, x_max + np.random.randint(0, 20))
        y_min = max(0, y_min - np.random.randint(0, 20))
        y_max = min(H, y_max + np.random.randint(0, 20))
        bbox = [x_min, y_min, x_max, y_max]

        return bbox
    except Exception as e:
        print(f"Error getting bounding box: {e}")
        return None

class SAMDataset(dt):
    def __init__(self, processor, dataset):
        self.processor = processor
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        try:
            item = self.dataset[idx]
            image_path = item["image"]
            contours = item["contours"]

            # Load image using Pillow
            image = Image.open(image_path)
            image = np.array(image)  # Convert PIL image to numpy array

            # Get image size
            image_height, image_width = image.shape[:2]

            # Convert contour points to integers
            contour_int = np.round(contours).astype(int)

            # Ensure that the contour is a list of arrays
            contour_list = [np.array(contour_int, dtype=np.int32)]

            # Create mask
            mask = np.zeros((image_height, image_width), dtype=np.uint8)
            cv2.fillPoly(mask, contour_list, 1)

            # Resize image and mask
            # resized_mask = cv2.resize(mask, (image_height, image_width))
            # ground_truth_mask = np.array(resized_mask)

            ground_truth_mask = mask
            prompt = get_bounding_box(ground_truth_mask)
            if prompt is None:
                return None
            inputs = self.processor(image, input_boxes=[[prompt]], return_tensors="pt")
            inputs = {k: v.squeeze(0) for k, v in inputs.items()}

            inputs["ground_truth_mask"] = ground_truth_mask

            return inputs
        except Exception as e:
            print(f"Error getting item from dataset: {e}")
            return {}  # Return an empty dictionary as a placeholder


if __name__ == "__main__":
    parser.add_argument('--image_dir', type=str, help='Path to the directory containing images')  
    args = parser.parse_args()  
    root_directory = args.image_dir

    all_images = []
    all_contours = []
    image_files = []

    if os.path.isdir(root_directory) is False:
        print(f"Input directory not found: {root_directory}. Skipping...")
    
    for root, sub_dirs, files in os.walk(root_directory):
        for direc in sub_dirs:
            sub_dir_path = os.path.join(root, direc)
            if direc == "train":
                curr_files = os.listdir(sub_dir_path)
                for file_ in curr_files:
                    full_path = os.path.join(sub_dir_path, file_)
                    image_files.append(full_path)
            else:
                image_directory_path = os.path.join(sub_dir_path, "train")
                if os.path.isdir(image_directory_path):
                    curr_files = os.listdir(image_directory_path)
                    for file_ in curr_files:
                        full_path = os.path.join(image_directory_path, file_)
                        image_files.append(full_path)

    for image_file in image_files:
        if image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            json_path = os.path.join(os.path.dirname(image_file), f"{os.path.splitext(os.path.basename(image_file))[0]}.json")

            if not os.path.exists(json_path):
                print(f"JSON file not found for image: {image_file}")
                continue

            contours, image_path = load_contours_from_json(json_path)
            all_contours.extend(contours)
            image_paths = [image_path] * len(contours)
            all_images.extend(image_paths)

    # Create a dataset
    dataset = Dataset.from_dict({
        'image': all_images,
        'contours': all_contours
    })

    # Create SAMDataset instance
    processor = SamProcessor.from_pretrained("facebook/sam-vit-base") # check 
    train_dataset = SAMDataset(dataset=dataset, processor=processor)

    # Create DataLoader
    train_dataloader = DataLoader(train_dataset, batch_size=2, shuffle=True)
    
    """Loading the model"""
    model = SamModel.from_pretrained("facebook/sam-vit-base")

    for name, param in model.named_parameters():
        if name.startswith("vision_encoder") or name.startswith("prompt_encoder"):
            param.requires_grad_(False)

    optimizer = Adam(model.mask_decoder.parameters(), lr=1e-5, weight_decay=0)
    seg_loss = monai.losses.DiceCELoss(sigmoid=True, squared_pred=True, reduction='mean')
    num_epochs = 10

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    model.train()
    for epoch in range(num_epochs):
        epoch_losses = []
        for batch in tqdm(train_dataloader):
            outputs = model(pixel_values=batch["pixel_values"].to(device),
                            input_boxes=batch["input_boxes"].to(device),
                            multimask_output=False)

            # compute loss
            predicted_masks = outputs.pred_masks.squeeze(1)
            ground_truth_masks = batch["ground_truth_mask"].float().to(device)

            # Resize ground truth masks to match the size of predicted masks
            ground_truth_masks_resized = F.interpolate(ground_truth_masks.unsqueeze(1),
                                                        size=predicted_masks.shape[-2:],
                                                        mode='nearest').squeeze(1)

            # Add an additional dimension to match the number of dimensions of predicted_masks
            ground_truth_masks_resized = ground_truth_masks_resized.unsqueeze(1)

            # Compute loss using resized ground truth masks
            loss = seg_loss(predicted_masks, ground_truth_masks_resized)

            # backward pass (compute gradients of parameters w.r.t. loss)
            optimizer.zero_grad()
            loss.backward()

            # optimize
            optimizer.step()
            epoch_losses.append(loss.item())

        print(f'EPOCH: {epoch}')
        print(f'Mean loss: {mean(epoch_losses)}')

        # Generate a timestamp for the current subdirectory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    model_path = f'./model_finetuned_{timestamp}.pth'
    # Save the trained model with timestamp in the file path
    torch.save(model.state_dict(), model_path)
    print(f"Model saved successfully at: {model_path}")

   
