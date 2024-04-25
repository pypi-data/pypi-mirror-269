# -------------------------------------------------------------------------------------
#  Originally Developed by :  Ignitarium Technology Solutions Pvt. Ltd.
#  This file is released under permissive terms. You may use,
#  modify, copy or distribute this file without restriction as long as this
#  section of the header (“Originally Developed by”) is retained
#  without modification.
# -------------------------------------------------------------------------------------
#  Filename    : finetune_infer.py
# -------------------------------------------------------------------------------------
#  Description : SAM finetune inference code
# -------------------------------------------------------------------------------------

"""Original SAM model inference code with boundind box approach"""
import os
import numpy as np
import random
import requests
import argparse
import torch
import cv2
import json
import torch.nn.functional as F

from segment_anything import SamPredictor, sam_model_registry
from transformers import SamModel, SamConfig, SamProcessor

class SAMFinetuneInference:
    def __init__(self, model_choice, device, checkpoint_path):
        """
        Initialize the SAMInference object.
        """
        model_config = SamConfig.from_pretrained("facebook/sam-vit-base")
        self.processor = SamProcessor.from_pretrained("facebook/sam-vit-base")

        # Create an instance of the model architecture with the loaded configuration
        self.sam = SamModel(config=model_config)
        # Load the fine-tuned weights
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.sam.load_state_dict(torch.load(checkpoint_path, map_location=device))

    def postprocess_masks(self, masks, input_size, original_size, image_size=1024):
        """
        Remove padding and upscale masks to the original image size.

        Args:
        masks (torch.Tensor):
            Batched masks from the mask_decoder, in BxCxHxW format.
        input_size (tuple(int, int)):
            The size of the image input to the model, in (H, W) format. Used to remove padding.
        original_size (tuple(int, int)):
            The original size of the image before resizing for input to the model, in (H, W) format.

        Returns:
        (torch.Tensor): Batched masks in BxCxHxW format, where (H, W)
            is given by original_size.
        """
        masks = F.interpolate(
            masks,
            (image_size, image_size),
            mode="bilinear",
            align_corners=False,
        )
        masks = masks[..., : input_size[0], : input_size[1]]
        masks = F.interpolate(masks, original_size, mode="bilinear", align_corners=False)
        return masks

    def get_contour(self, masks):
        """
        Generate contour from given masks.
        Attributes
            masks (tensor): Masks output from SAM
        """
        count = 0
        segmentations = []
        areas = []
        bboxes = []
        for mask in masks:
            # Find contours in the mask image
            count += 1
            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
            )
            contour = max(contours, key=len)
            # calculate area
            area = int(cv2.contourArea(contour))
            if area > 0:
                # Convert the (x, y) pairs to a list of integers
                segmentations.append((contour,))
                areas.append(area)
                x_coordinate, y_coordinate, width, height = cv2.boundingRect(contour)
                start_x, start_y, end_x, end_y = (
                    x_coordinate,
                    y_coordinate,
                    x_coordinate + width,
                    y_coordinate + height,
                )
                bboxes.append([int(start_x), int(start_y), int(end_x), int(end_y)])
        return segmentations, areas, bboxes

    def infer(self, image_data, boxes):
        # Prepare image + box prompt for the model
        inputs = self.processor(image_data, input_boxes=[boxes[0].tolist()], return_tensors="pt").to(device)

        # Forward pass
        with torch.no_grad():
            output = self.sam(**inputs, multimask_output=False)
            iou, masks = output[0], output[1]

        masks = self.postprocess_masks(masks[0], (800, 800), (800, 800), 800)
        masks = masks.cpu().numpy().squeeze()
        masks = (masks > 0.5).astype(np.uint8)

        segmentations, areas, bboxes = self.get_contour(masks)
        annotation = {
            "segmentation": segmentations,
            "area": np.array(areas, dtype=np.float32),
            "bbox": np.array(bboxes, dtype=np.float32),
            "sam_conf": np.array(iou.cpu(), dtype=np.float32),
        }

        return annotation

