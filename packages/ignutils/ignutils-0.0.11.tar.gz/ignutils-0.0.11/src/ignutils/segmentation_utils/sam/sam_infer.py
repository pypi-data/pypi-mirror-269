# -------------------------------------------------------------------------------------
#  Originally Developed by :  Ignitarium Technology Solutions Pvt. Ltd.
#  This file is released under permissive terms. You may use,
#  modify, copy or distribute this file without restriction as long as this
#  section of the header (“Originally Developed by”) is retained
#  without modification.
# -------------------------------------------------------------------------------------
#  Filename    : sam_infer.py
# -------------------------------------------------------------------------------------
#  Description : SAM segmentation inference code
# -------------------------------------------------------------------------------------

"""Original SAM model inference code with boundind box approach"""
import os
import numpy as np
import random
import requests
import argparse
import torch
import cv2
import sys
import unittest

from segment_anything import SamPredictor, sam_model_registry

class SAMInference:
    """
    SAMInference performs instance segmentation with Segment Anything Model
    on given data.

    This class takes care of loading the model, processing input data,
    and generating segmentation results.

    Attributes:
        work_dir (str): The path of working directory (pose_app).
        model_choice (str): The model choice for sam. One of vit_b, vit_h, vit_l.
        device (torch object): The hardware device (CPU/CUDA) for running inference.

    Methods:
        select_model: Determine checkpoints path based on given model choice and download weights.
        get_contour: Generate contour for given mask.
        infer: Perform inference on given data and check validity for box size
    """

    def __init__(self, model_choice, device, checkpoint_path=None):
        """
        Initialize the SAMInference object.
        """
        self.model_choice = model_choice
        self.checkpoint_path = self.select_model(self.model_choice, checkpoint_path)

        try:
            self.sam = sam_model_registry[self.model_choice](
                checkpoint=self.checkpoint_path
            )
        except:
            os.remove(self.checkpoint_path)
            self.checkpoint_path = self.select_model(self.model_choice, checkpoint_path)
            self.sam = sam_model_registry[self.model_choice](
                checkpoint=self.checkpoint_path
            )

        self.device = device
        print("[INFO] SAM weights loaded sucessfully")
        self.sam.to(device=device)

    def select_model(self, model_choice, checkpoint_path):
        """
        Chooce checkpoint path and download weights if not available.
        Attributes:
            model_choice (str): The model choice for sam. One of vit_b, vit_h, vit_l.
        Returns:
            checkpoint_path (str): The path of model checkpoint file in local storage.
        """
        if checkpoint_path is None:
            checkpoint_path = ""
        if model_choice == "vit_b":
            checkpoint_url = (
                "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth"
            )
            checkpoint_path = os.path.join(checkpoint_path, "sam_vit_b_01ec64.pth")
        elif model_choice == "vit_l":
            checkpoint_url = (
                "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth"
            )
            checkpoint_path = os.path.join(checkpoint_path, "sam_vit_l_0b3195.pth")
        elif model_choice == "vit_h":
            checkpoint_url = (
                "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
            )
            checkpoint_path = os.path.join(checkpoint_path, "sam_vit_h_4b8939.pth")
        elif model_choice == "edge_sam":
            checkpoint_url = "https://huggingface.co/spaces/chongzhou/EdgeSAM/resolve/main/weights/edge_sam.pth"
            checkpoint_path = os.path.join(checkpoint_path, "edge_sam.pth")
        elif model_choice == "edge_sam_3x":
            checkpoint_url = "https://huggingface.co/spaces/chongzhou/EdgeSAM/resolve/main/weights/edge_sam_3x.pth"
            checkpoint_path = os.path.join(checkpoint_path, "edge_sam_3x.pth")
            self.model_choice = "edge_sam"
        else:
            raise ValueError(
                "Wrong model type for SAM."
                + "Please choose model from ['vit_b', 'vit_l', 'vit_h', 'edge_sam', 'edge_sam_3x']"
                + "Check help (-h) for more details"
            )
        if not os.path.exists(checkpoint_path):
            print("[INFO] Downloading SAM weights")
            response = requests.get(checkpoint_url, stream=True, timeout=10)
            response.raise_for_status()
            with open(checkpoint_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            print("[INFO] Weights downloaded")
        return checkpoint_path

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
            mask = mask.cpu().numpy().squeeze().astype(np.uint8)
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
        """
        Perform instance segmentation on input image.
        Attributes
            input_data (numpy): Input image in numpy format.
            boxes (array): Bounding boxes for given image.
        Returns:
            annotation (dict): Dictionary containing contours, area and tight bounding box
        """
        predictor = SamPredictor(self.sam)
        predictor.set_image(image_data)
        boxes = torch.tensor(boxes, device=self.device)
        boxes = predictor.transform.apply_boxes_torch(boxes, image_data.shape[:2])
        masks, iou, _ = predictor.predict_torch(
            point_coords=None,
            point_labels=None,
            boxes=boxes,
        )
        avg_ious = torch.mean(iou, dim=0)
        best_iou = torch.argmax(avg_ious).item()
        masks = masks[:, best_iou : best_iou + 1, :, :]
        iou = iou[:, best_iou : best_iou + 1]

        segmentations, areas, bboxes = self.get_contour(masks)
        annotation = {
            "segmentation": segmentations,
            "area": np.array(areas, dtype=np.float32),
            "bbox": np.array(bboxes, dtype=np.float32),
            "sam_conf": np.array(iou.cpu(), dtype=np.float32),
        }
        return annotation


class TestSegmentationUtils(unittest.TestCase):
    """test sam infer"""

    def test_sam_infer(self):
        """test sam infer with test image and json"""
        from ignutils.draw_utils import draw_polylines
        from ignutils.json_utils import read_json

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        sam_obj = SAMInference(
            model_choice="vit_b",
            device=device
        )
        test_image = cv2.imread("samples/sam_infer.jpg")
        assert test_image is not None, "Could not read image. Please check path again"
        bbox_json = read_json("samples/sam_infer.json")
        boxes = bbox_json['shapes'][0]['points']
        annotations = sam_obj.infer(image_data=test_image, boxes=boxes)

        contours = annotations["segmentation"]
        assert len(contours) > 0, "Test Failed, contours not found!"
        bounding_boxes = annotations["bbox"]
        for contr in contours:
            seg_result = draw_polylines(test_image.copy(), contr[0], color=[0, 0, 255], thickness=2)
        save_path = os.path.join("samples", "test_results", "seg_result.jpg")
        cv2.imwrite(save_path, seg_result)


if __name__ == "__main__":
    test_obj = TestSegmentationUtils()
    test_obj.test_sam_infer()

