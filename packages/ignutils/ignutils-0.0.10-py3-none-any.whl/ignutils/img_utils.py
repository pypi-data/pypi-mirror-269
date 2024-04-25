# --------------------------------------------------------------------------
#                         Copyright © by
#           Ignitarium Technology Solutions Pvt. Ltd.
#                         All rights reserved.
#  This file contains confidential information that is proprietary to
#  Ignitarium Technology Solutions Pvt. Ltd. Distribution,
#  disclosure or reproduction of this file in part or whole is strictly
#  prohibited without prior written consent from Ignitarium.
# --------------------------------------------------------------------------
#  Filename    : img_utils.py
# --------------------------------------------------------------------------
"""To do basic image operations on images and sanity checks for files and directories."""

import os
import os.path as osp
import base64
import unittest
from imgaug import augmenters as iaa
import cv2
import numpy as np
from skimage.morphology import skeletonize

import ignutils as icv
from ignutils.contour_utils import get_contours, rescale_json, cv2lab
from ignutils.show_utils import show
from ignutils.typehint_utils import Mat
from ignutils.json_utils import read_json, write_json
from ignutils.draw_utils import draw_polylines
from ignutils.file_utils import create_directory_safe, get_file_name, make_file_path


def do_sometimes(q):
    """The funtion get the a probability value as input and 
    Returns True or False based on this probability value"""
    if q == 0:
        return False
    if q == 1:
        return True
    r = np.random.choice([False, True], 1, p=[1 - q, q])
    return r


def compare_imgs(im1_path, im2_path, assert_flag=True):
    """Compare the two input images
    Args:
        im1_path: Path of image1
        im2_path: PAth of image2
    Returns:
        True if both are same else False
    """
    im1 = cv2.imread(im1_path)
    im2 = cv2.imread(im2_path)
    print("im1:", im1.shape)
    print("im2:", im1.shape)
    comparison = im1 == im2
    equal_arrays = comparison.all()
    # breakpoint()
    if assert_flag:
        assert equal_arrays, "images not matching"
    return equal_arrays


def img_decode(img):
    """Returns the decoded image with base64"""
    img1_bytes_ = base64.b64decode(img)
    img1_bytes_ = np.frombuffer(img1_bytes_, np.uint8)
    img = cv2.imdecode(img1_bytes_, 1)
    return img

def rgb2hex(color):
    """To convert rgb to hex."""
    r, g, b = color
    return f"#{r:02x}{g:02x}{b:02x}"

def hex2rgb(hexcode):
    """To convert hexcode to r, g, b"""
    return tuple(map(ord, hexcode[1:].decode("hex")))


def get_iou(gt_mask, pred_mask, iou_method="mask_and", box_wd=10, box_ht=10):  # To-do: implement using shapely
    """To get Inersection area, union_area and IOU score of the ground truth and pred_mask image.
    Args:
        gt_mask : ground truth mask
        pred_mask : Prediction mask
        iou_method : Type of IOU method to use for getting
            intersection area, defaults to "mask_and"
        box_wd : box width to use for calculating intersection
            area, defaults to 10
        box_ht : height to use for calculating intersection area,
            defaults to 10
    Returns:
        inter_area: intersection area between the gt and pred
        union_area: union area between the gt and pred
        iou_score: IOU value
    """
    if gt_mask is None or pred_mask is None:
        return 0
    if np.count_nonzero(gt_mask) == 0:
        max_area = np.sum(np.ones(gt_mask.shape, dtype=bool))
        union_area = np.sum(np.logical_or(gt_mask, pred_mask))
        diff_area = max_area - union_area
        iou_score = diff_area / max_area
        return 0, union_area, iou_score
    if iou_method == "mask_pool":
        inter_area_canvas = custom_and_op(pred_mask, gt_mask, box_wd=box_wd, box_ht=box_ht)
        inter_area = np.count_nonzero(inter_area_canvas)
    else:
        inter_area = np.logical_and(gt_mask, pred_mask)
    union_area = np.logical_or(gt_mask, pred_mask)
    inter_area = np.sum(inter_area)
    union_area = np.sum(union_area)
    iou_score = inter_area / union_area
    return inter_area, union_area, iou_score


def custom_and_op(pred_mask, gt_mask, box_wd=10, box_ht=10):  # Remove this once get_iou is removed
    """custom and op"""
    H, W = gt_mask.shape[:2]
    indices = np.where(gt_mask == [255])
    canvas = np.zeros((H, W, 1))
    # box_wd // 2
    # box_ht // 2
    for i in range(len(indices[0])):
        # np.where returns 1st dimension, followe by 2nd dim
        y, x = indices[0][i], indices[1][i]
        x1 = max(0, (x - box_wd // 2))
        x2 = min(W, (x + box_wd // 2))

        y1 = max(0, (y - box_ht // 2))
        y2 = min(H, (y + box_ht // 2))

        pred_roi = pred_mask[y1:y2, x1:x2]
        if np.count_nonzero(pred_roi):
            canvas[y, x, :] = [255]
    return canvas


def rotate_bound(image, angle):
    """Rotate an image without croppping
    Returns the rotated image and rotation matrix"""
    (h, w) = image.shape[:2]
    (c_x, c_y) = (w // 2, h // 2)

    tr = cv2.getRotationMatrix2D((c_x, c_y), -angle, 1.0)
    cos = np.abs(tr[0, 0])
    sin = np.abs(tr[0, 1])
    n_w = int((h * sin) + (w * cos))
    n_h = int((h * cos) + (w * sin))

    tr[0, 2] += (n_w / 2) - c_x
    tr[1, 2] += (n_h / 2) - c_y
    rotated_img = cv2.warpAffine(image, tr, (n_w, n_h))
    return rotated_img, tr


def is_video(filenam):
    """Check if its a video file"""
    if os.path.splitext(filenam)[1].lower() in [".mp4", ".mov", ".avi", ".wmv", ".mkv", ".webm", ".wmv", ".flv", ".f4v", ".avchd"]:
        return True
    return False


def area_filter(contours, threshold_area):
    """Function checks if countour area of the given contours
    is greater than threshold area provided.
    Returns: 
        List of contours having area greater than threshold area.
    """
    contours_out = []
    for c in contours:
        if cv2.contourArea(c) > threshold_area:
            contours_out.append(c)
    return contours_out


def get_line_dim(image):
    """Given an image, get crack width, crack thickness."""
    crop_contours, hierarchy = get_contours(image)
    scale_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, bw_img = cv2.threshold(scale_gray, 0, 255, cv2.THRESH_BINARY)
    bw_img1 = bw_img.astype(np.float64)
    area_orginal = np.sum(bw_img1 / 255.0)
    skeleton_lee = skeletonize(bw_img, method="lee")
    skeleton_lee1 = skeleton_lee.astype(np.float64)
    skeleton_length = np.sum(skeleton_lee1 / 255.0)
    if skeleton_length:
        thickness = area_orginal / skeleton_length
    else:
        thickness = 0
    if thickness > skeleton_length:
        skeleton_length, thickness = thickness, skeleton_length
    if crop_contours is None:
        crop_contours = []
    return thickness, skeleton_length, crop_contours, area_orginal


def stitch_to_background(background_img, foreground_img, foreground_mask):
    """Stitch the foreground image to the background image using the foreground mask.
    Returns the stitched image"""
    background_img_copy = background_img.copy()
    foreground_mask[foreground_mask[:, :, 0] == 255] = 255
    mask = foreground_mask[:, :, :] == 255
    background_img_copy[mask] = foreground_img[mask]
    return background_img_copy


def get_image_overlay(img, mask, transparency=0.7):
    """Returns image after overlaying mask on image"""
    img = np.array(img, dtype=np.float32)
    img /= 255.0
    mask = np.array(mask, dtype=np.float32)
    mask /= 255.0
    mask *= transparency
    out = mask + img * (1.0 - mask)
    return out

def custom_fog_augmentation():
    """custom fog aumentation with imgaug for keras training"""
    return iaa.Fog()

def get_transparent_image(img, mask, alpha=0.3, color=(0, 255, 0)):
    """get transparent overlay image using mask and mask_inv,
    multiplying and adding fused image and original image
    if mask is single channel, result will be in given color
    Returns an image with the mask overlayed
    """
    if len(mask.shape) == 3:
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, mask_b = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_color = mask
    else:
        mask_b = mask * 255
        mask_color = np.zeros_like(img)
        mask_color[mask == 1] = color
    mask_b = np.stack((mask_b,) * 3, axis=-1)
    mask_b_inv = cv2.bitwise_not(mask_b)
    image_mask = cv2.bitwise_and(img, mask_b_inv)
    fused = cv2.addWeighted(mask_color, alpha, img, 1 - alpha, 0, img)
    fused_mask = cv2.bitwise_and(fused, mask_b)
    final_out = cv2.add(image_mask, fused_mask)
    return final_out


def get_padding_on_boxlist(boxlist, pad_val):
    """Given list of box, return a list of padded box."""
    new_box = []
    if len(boxlist):
        for box in boxlist:
            x, y, w, h = box
            x1, y1, w1, h1 = x + pad_val, y, w, h
            new_box.append([x1, y1, w1, h1])
    return new_box


def draw_rect_from_xywh(image, boxlist, color=(0, 255, 0), thickness=6, xywh=True):
    """Given image and boxlist, function will draw a rectangle over the ROI"""
    if len(boxlist) > 0:
        for box in boxlist:
            if len(box):
                x1, y1 = box[:2]
                if xywh:
                    width = box[2]
                    height = box[3]
                    x2 = x1 + width
                    y2 = y1 + height
                else:
                    x2, y2 = box[2:]
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness)
    return image


def check_label_dict(json_dict, labelnames):
    """Returns True if label exist in json dict"""
    shape_list = json_dict["shapes"]
    for shape_dict in shape_list:
        if shape_dict["label"] in labelnames:
            return True
    return False


def dump_image_batch(node_config, filename, foldername, images_list, masks_list, empty_prob=1, neg_label_prob=1, ht_thresh=None, wd_thresh=None, json_list=None, debug_level=0, img_quality=100):
    """Process list of images list, masks list and dumps it to given folder."""
    # if not check_folder_exists(foldername):
    # create_directory_safe(foldername)
    # print(f"'{foldername}' Exist!!")
    end_folder = os.path.basename(foldername)
    dir_path = os.path.dirname(foldername)
    basename_ = os.path.basename(dir_path)
    dst_folder = os.path.dirname(os.path.dirname(dir_path))
    repo_folder = os.path.basename(os.path.dirname(dir_path))
    small_dump_folder = None
    fused_foldername = None
    if node_config("fused_dump") or debug_level > 0:
        fused_foldername = basename_ + "_fused"
        fused_folder = os.path.join(dst_folder, fused_foldername, repo_folder, end_folder)
        ignored_foldername = basename_ + "Ignored"
        small_dump_folder = os.path.join(dst_folder, ignored_foldername, repo_folder, end_folder)

    basename = get_file_name(filename)
    if json_list is not None:
        assert len(json_list) == len(images_list)
    if node_config("train_dump_extension"):
        img_extension = node_config("train_dump_extension")
    else:
        img_extension = ".jpg"

    for i, image in enumerate(images_list):
        write_flag = True
        height, width = image.shape[:2]
        mask = masks_list[i]

        if json_list:
            json_dict = json_list[i]
            json_dict["org_dim"] = [height, width]  # storing crop image org dimension
        else:
            json_dict = None

        if not np.any(mask):  # dump based on probability
            neg_label_list = node_config("negative_co_labels")
            write_flag = False
            name_no_ext = ""
            if not check_label_dict(json_dict, neg_label_list):  # if empty file dump based on empty_probability from config
                if do_sometimes(empty_prob):
                    name_no_ext = f"--{i}--empty_neg"
                    write_flag = True
            else:  # if neg co labels present dump with neg_colabel probability
                if do_sometimes(neg_label_prob):
                    name_no_ext = f"--{i}--label_neg"
                    write_flag = True

        else:
            name_no_ext = f"--{i}"

        if ht_thresh and wd_thresh:
            if not (image.shape[0] > ht_thresh or image.shape[1] > wd_thresh):
                if debug_level > 0:
                    create_directory_safe(small_dump_folder)
                    file_name_image = osp.join(small_dump_folder, basename + f"{name_no_ext}.jpg")
                    cv2.imwrite(file_name_image, image, [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])
                continue

        if node_config("resize_factor") is not None and node_config("tiling_mode") is not None:
            resize_factor = node_config("resize_factor")
            model_input_h, model_input_w = node_config("model_input_HW")
            expansion_input_h, expansion_input_w = node_config("train_extra_expansion")
            resize_h = int((model_input_h + expansion_input_h) * resize_factor)
            resize_w = int((model_input_w + expansion_input_w) * resize_factor)

            image = cv2.resize(image, (resize_w, resize_h), interpolation=cv2.INTER_NEAREST)
            mask = cv2.resize(mask, (resize_w, resize_h), interpolation=cv2.INTER_NEAREST)
            json_dict = rescale_json(json_dict, height, width, resize_h, resize_w)

        root_path = osp.join(dst_folder, basename_)
        create_directory_safe(root_path)
        fused_root_path = osp.join(dst_folder, fused_foldername)
        create_directory_safe(fused_root_path)

        parent_contour_name = node_config("parent_contour")
        if parent_contour_name:
            lable_name = parent_contour_name
        else:
            lable_name = "Full"

        if write_flag:
            if img_extension == ".jpg":
                file_name_image = osp.join(foldername, basename + name_no_ext + img_extension)
                file_name_image = make_file_path(file_path=file_name_image, source_path=dst_folder)
                file_name_image = lable_name + "--" + file_name_image + img_extension
                file_path = osp.join(root_path, file_name_image)
                cv2.imwrite(file_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), img_quality])
            else:
                file_name_image = osp.join(foldername, basename + f"{name_no_ext}.png")
                file_name_image = make_file_path(file_path=file_name_image, source_path=dst_folder)
                file_name_image = lable_name + "--" + file_name_image + img_extension
                file_path = osp.join(root_path, file_name_image)
                cv2.imwrite(file_path, image, [int(cv2.IMWRITE_PNG_COMPRESSION), 100 - img_quality])

            if json_dict is not None:
                json_dict["imagePath"] = osp.basename(file_name_image)
                json_dump_name = osp.join(foldername, basename + f"{name_no_ext}.json")
                json_dump_name = make_file_path(file_path=json_dump_name, source_path=dst_folder)
                json_dump_name = lable_name + "--" + json_dump_name + ".json"
                json_dump_path = osp.join(root_path, json_dump_name)
                write_json(json_dump_path, json_list[i])
            if node_config("fused_dump"):
                fused = get_transparent_image(image, mask)
                file_name_fused = osp.join(fused_folder, basename + f"{name_no_ext}.jpg")
                file_name_fused = make_file_path(file_path=file_name_fused, source_path=fused_root_path)  # , dst_path= fused_root_path,ext = ".jpg")
                file_name_fused = lable_name + "--" + file_name_fused + ".jpg"
                file_fused_path = osp.join(fused_root_path, file_name_fused)
                cv2.imwrite(file_fused_path, fused)
                if debug_level > 0:
                    show(fused, "Crop_fused")
            if debug_level > 0:
                show(image, "Crop_image")


def find_cv_contours(image):
    """Returns contours in the input image"""
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 10, 255, 0)
    cv_contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv_contours = [cv2lab(cont) for cont in cv_contours]
    return cv_contours


def pad_image(img, top=0, bottom=0, left=0, right=0):
    """Returns the padded the input image with zeros on all sides."""
    padded = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return padded


def pad_image_h_w(img, H, W):
    """Pad the input image with zeros to get the same height and width as the input H and W
    Returns the padded image with matches the input image dimensions
    """
    pad_top_bottom = H - img.shape[0]
    pad_top = int(pad_top_bottom / 2)
    pad_bottom = pad_top_bottom - pad_top
    pad_left_right = W - img.shape[1]
    pad_left = int(pad_left_right / 2)
    pad_right = pad_left_right - pad_left
    padded = cv2.copyMakeBorder(img, top=pad_top, bottom=pad_bottom, left=pad_left, right=pad_right, borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return padded


def check_same_img(im1: Mat, im2: Mat, max_count: int = 0) -> bool:
    """Check if two input images are the same"""
    diff = im1 - im2
    diff_count = np.count_nonzero(diff)
    if diff_count > max_count:
        return False
    return True

