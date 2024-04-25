# -------------------------------------------------------------------------------------
#  Originally Developed by :  Ignitarium Technology Solutions Pvt. Ltd.
#  This file is released under permissive terms. You may use,
#  modify, copy or distribute this file without restriction as long as this
#  section of the header (“Originally Developed by”) is retained
#  without modification.
# -------------------------------------------------------------------------------------
#  Filename    : contour_utils.py
# -------------------------------------------------------------------------------------
"""To do basic operations (such as finding magnitude, 
getting x and y location for based on image positions etc.,) 
for a given contour information.

Run: python3 -m ignutils.contour_utils
"""

import math
import unittest
from typing import List

import cv2
import numpy as np
from fabulous import color
from shapely.geometry import Polygon
from shapely.ops import unary_union

from ignutils.draw_utils import draw_polylines
from ignutils.typehint_utils import CntrL, CntrC, Cntr, Optional
from ignutils.geom_utils import get_translation_matrix
from ignutils.labelme_utils import create_labelme_json
from ignutils.geom_utils import euclidean

# import logging
# logging.basicConfig(level=logging.ERROR)


def rotate(point, angle_deg=math.radians(90), origin=(0, 0)):
    """Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    Returns the rotated point
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle_deg) * (px - ox) - math.sin(angle_deg) * (py - oy)
    qy = oy + math.sin(angle_deg) * (px - ox) + math.cos(angle_deg) * (py - oy)
    return qx, qy


def rotate_json(json_dict, rot_matrix):
    """rotate all contours in json dict using the rotation matrix
    Returns the json dict with rotated contours    
    """
    shapes = json_dict["shapes"]
    for shape in shapes:
        cntr = shape["points"]
        rotated_cntr = rotate_contour(cntr, rot_matrix)
        if isinstance(rotated_cntr, np.ndarray):
            rotated_cntr = cv2lab(rotated_cntr)
        shape["points"] = rotated_cntr
    return json_dict


def rotate_contour(contour, rot_matrix):
    """Rotate the given contour based on rotation matrix
    Returns the rotated contour
    """
    if isinstance(contour, list):  # check inp contour is opencv format numpy array or labelme list
        point_list = lab2cv(contour)
    rotated_cntr = cv2.transform(point_list, rot_matrix)
    if isinstance(contour, list):
        rotated_cntr = cv2lab(rotated_cntr)
    return rotated_cntr


def getboxangle(box):
    """Returns the angle of the box."""
    tl, tr, br, bl = box
    ydist = bl[1] - tl[1]
    xdist = bl[0] - tl[0]
    if xdist:
        slope = ydist / xdist
        boxangle = math.degrees(math.atan(slope))
    else:
        boxangle = 90
    return boxangle


def calculate_iou(contour1, contour2):
    """Returns the iou of the two given contours"""
    polygon1 = Polygon(contour1)
    polygon2 = Polygon(contour2)
    intersect = polygon1.intersection(polygon2).area
    union = polygon1.union(polygon2).area
    iou = intersect / union
    return iou


def translate_points(points, x, y):
    """Returns the shifted contour based on the x and y values provided"""
    pt = np.array((x, y))
    shifted_points = np.add(pt, points)
    shifted_points = shifted_points.tolist()
    return shifted_points


def shift_cntrs(cntrs_list: list, shift_x: int, shift_y: int) -> list:
    """Inplace shift of the contours in cntrs_list based on shift_x, shift_y respectively.
    Args:
        cntrs_list (list): List of input contours
        shift_x (int): Increment x-coordinate by this value in cntrs_list
        shift_y (int): Increment y-coordinate by this value in cntrs_list
    Returns:
        List of shifted contours
    """
    shifted_list = []
    for i, cntr in enumerate(cntrs_list):
        cntr = np.array(cntr)
        cntr[:, 0] += shift_x
        cntr[:, 1] += shift_y
        contr = cntr.tolist()
        shifted_list.append(contr)
    return shifted_list


def shift_json(json_dict, tr_matrix):
    """shift/translate all contours in json dict
    Returns the json dict with all shifted contours
    """
    shapes = json_dict["shapes"]
    for shape in shapes:
        cntr = shape["points"]
        rotated_cntr = translate_contour(cntr, tr_matrix)
        if isinstance(rotated_cntr, np.ndarray):
            rotated_cntr = cv2lab(rotated_cntr)
        shape["points"] = rotated_cntr
    return json_dict

def transform_contour(point_list, tr):
    """Function to apply transform matrix on point list
    Args:
        point_list : list of points
        tr : Transformation matrix
    Returns:
        points after transformation
    """
    tr = np.array(tr, dtype=np.float64)
    contours = np.array([point_list], dtype=np.float32)
    if tr.shape == (2, 3):
        out_point_list = cv2.transform(contours, tr)
    else:
        out_point_list = cv2.perspectiveTransform(contours, tr)  # .astype(int)
    out_point_list = np.squeeze(out_point_list).astype(np.float32)
    return out_point_list

def get_tiled_contours(contour, crop_type, tiling_info):
    """split inp contours in tiles"""

    if tiling_info.get("tiling_mode") is None:
        return [contour], [contour]
    src_pts = get_box(contour, crop_type=crop_type)
    h1, w1 = get_box_dims(src_pts)
    # img_copy = img.copy()
    # im_drw = draw_polylines(img_copy, src_pts)
    # im_draw = draw_polylines(im_drw, contour, color = (0,255,0))
    dst_points = np.array([[0, 0], [w1, 0], [w1, h1], [0, h1]], dtype=np.float32)
    inv_tr = cv2.getPerspectiveTransform(dst_points, src_pts)
    tile_loc_list = split_tiles(dst_points, tiling_info)
    transformed_tile_loc = []
    for tile_loc in tile_loc_list:
        x1,y1,x2,y2 = tile_loc
        tile_loc = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        tile_loc_ = transform_contour(tile_loc, inv_tr)
        transformed_tile_loc.append(tile_loc_)

    tiled_contours = []
    for tile_loc in transformed_tile_loc:
        # im_draw = draw_polylines(im_draw, tile_loc, color = (0,0,255))
        tile_cntrs = get_contour_intersection(tile_loc, contour)
        # if any(tile_cntrs):
        #     im_draw = draw_polylines(im_draw, tile_cntrs, color = (255,0,0))
        for tile_cntr in tile_cntrs:
            tiled_contours.append(tile_cntr)
    # cv2.imwrite(f"img_{time.time()}.jpg", im_draw)
    return tiled_contours, transformed_tile_loc

def rescale_contour(contour, height, width, target_height, target_width):
    """rescaling contours based on the target height and width provided
    Returns the rescaled contour
    """
    x_scale = target_width / width
    y_scale = target_height / height
    if not isinstance(contour, np.ndarray):
        contour = np.array(contour)
    if len(contour.shape) > 2:
        contour = np.squeeze(contour)
    contour[:, 0] = x_scale * contour[:, 0]
    contour[:, 1] = y_scale * contour[:, 1]
    contour = contour.tolist()
    return contour


def rescale_json(json_dict, height, width, target_height, target_width):
    """Rescale all the contours in the json shapes dict based
    on the target height and width provided
    Returns the json dict with all the rescaled contour
    """
    shapes_list = json_dict["shapes"]
    for i, shape_dict in enumerate(shapes_list):
        shape_dict["points"] = rescale_contour(shape_dict["points"], height, width, target_height, target_width)
    json_dict["imageHeight"] = target_height
    json_dict["imageWidth"] = target_width
    return json_dict


def translate_contour(contour, tr_matrix):
    """Returns the shifted/translated contour based on tr matrix"""
    if isinstance(contour, list):  # check inp contour is opencv format numpy array or labelme list
        point_list = lab2cv(contour)
    translated_cntr = cv2.transform(point_list, tr_matrix)
    if isinstance(contour, list):
        translated_cntr = cv2lab(translated_cntr)
    return translated_cntr


def find_best_match(contour: Cntr, cntr_list: List[Cntr]):
    """Return best match index for cntrA from cntr_list based on the overlap area"""
    max_overlap_area = 0
    best_match_index = None
    for index, cntr in enumerate(cntr_list):
        overlap_area = get_overlap_area(np.array(contour).squeeze(), np.array(cntr).squeeze())
        if overlap_area > max_overlap_area:
            max_overlap_area = overlap_area
            best_match_index = index
    return best_match_index, max_overlap_area


def getbbox(cnt, unitvec=(0, 1), verticalfirst: Optional[bool] = True):
    """Returns bounding box points for the given contour,
    verticalfirst = True/False/None
    If its true, vertically sorting is done first.
    """
    x1, y1, w, h = cv2.boundingRect(cnt)
    x2 = x1 + w
    y2 = y1 + h
    box = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    if verticalfirst is not None:
        box = direction_boxsort(box, unitvec, verticalfirst)
    return box


def getfitbox(cnt, unitvec=(0, 1), verticalfirst: Optional[bool] = True):
    """Returns a fit bounding box around the given contour
    verticalfirst = True/False/None
    If its true, vertically sorting is done first.
    """
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.array(box, dtype=np.float32)
    if verticalfirst is not None:
        box = direction_boxsort(box, unitvec, verticalfirst)
    return box


def direction_boxsort(boxpoints, unit_vec=(0, 1), vertical_sort_first=True):
    """For sorting all the points in a specific direction provide vertical
    unitvec when vertical first is true ,else provide Horizontal unit vec.
    Args:
        boxpoints : contour points of type float32
        vertical_sort_first: sort along unit vec first if True
        unit_vec: the unit vector in the direction of sort is desired in tuple format , direction from btm to top
    Returns:
        Sorted points
    """
    normal_vec = rotate(unit_vec, angle_deg=math.radians(-90))
    if vertical_sort_first:
        sorted_list = sorted(boxpoints, key=lambda coord: np.dot(coord, unit_vec))
        first_pts = sorted_list[:2]
        second_pts = sorted_list[2:]
        tl, tr = sorted(first_pts, key=lambda coord: np.dot(coord, normal_vec))
        bl, br = sorted(second_pts, key=lambda coord: np.dot(coord, normal_vec))
    else:
        sorted_list = sorted(boxpoints, key=lambda coord: np.dot(coord, normal_vec))
        first_pts = sorted_list[:2]
        second_pts = sorted_list[2:]
        tl, bl = sorted(first_pts, key=lambda coord: np.dot(coord, unit_vec))
        tr, br = sorted(second_pts, key=lambda coord: np.dot(coord, unit_vec))
    return np.array([tl, tr, br, bl])


def get_contours(
    img,
    morphology_op=None,
    hull=False,
    kernel=3,
    convert_gray=True,
    thresholding=True,
):
    """Function to get all contours in an image with/without morphological
    operations based on inputs provided
    Returns:
        contours = list of contours present in mask with length
        hierarchy = list of hierarchy present in mask with length
    """
    img = img.astype(np.uint8)
    contours, hierarchy = None, None
    if convert_gray:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if np.any(img):
        if thresholding:
            _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

        if morphology_op is not None:
            kernel = np.ones(kernel, np.uint8)
            morph_operation = eval(str("cv2." + morphology_op)) # pylint: disable=eval-used
            img = cv2.morphologyEx(img, morph_operation, kernel)
        if cv2.__version__.split(".")[0] == str(3):
            _, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # cv2.CHAIN_APPROX_SIMPLE
        else:
            contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if hull and contours is not None:
        # epsilon = 0.001*cv2.arcLength(np.array(cnt),True)
        # contours[i] = cv2.approxPolyDP(np.array(cnt),epsilon,True)
        contours = [cv2.convexHull(np.array(cont)) for cont in contours]
        contours = [cv2lab(cont) for cont in contours]
    return contours, hierarchy


def get_bbox_from_contour(contour):
    """Function to get bbox i.e.,[x1,y1,x2,y2] points for the contour.
    Returns the bounding box
    """
    bbox = None
    bbox = cv2.boundingRect(contour)
    if bbox is not None:
        x, y, w, h = bbox
        bbox = [x, y, x + w, y + h]
    return bbox


def get_mask_from_json(json_dict, class_list, thickness=None, thickness_factor=1, color_list=None, H=None, W=None, mask=None):
    """
    To get the mask of an image from the json file provided.
    Args:
        json_dict: labelme json dictionary
        class_list: ['class1', 'class2']
        color_list: [[color1], [color2]]
    Returns:
        the mask of the image
    """
    all_points = []
    shape_info = json_dict.get("shapes", [])
    if H is None:
        H = json_dict["imageHeight"]
    else:
        json_dict["imageHeight"] = H
    if W is None:
        W = json_dict["imageWidth"]
    else:
        json_dict["imageWidth"] = W
    if mask is None:
        canvas = np.zeros((H, W, 3), np.uint8)
    else:
        canvas = mask
    for node_dict in shape_info:
        label = node_dict["label"]
        if label not in class_list:
            continue
        if color_list is not None:
            color_draw = color_list[class_list.index(label)]
        else:
            color_draw = [255, 255, 255]
        points = node_dict["points"]
        points = np.array(points).astype(int).tolist()
        label_type = node_dict["shape_type"]

        if label_type == "polygon":
            if len(points) == 2:
                cv2.rectangle(canvas, tuple(points[0]), tuple(points[1]), color_draw, -2)
            else:
                canvas = draw_polylines(canvas, points, fill=True, color=color_draw)

        elif label_type == "linestrip":
            if thickness is not None:
                thickness *= thickness_factor
            else:
                thickness = 2
            for i in range(len(points) - 1):
                start_point = points[i]
                end_point = points[i + 1]
                cv2.line(canvas, tuple(start_point), tuple(end_point), color_draw, thickness)
        else:
            print(color.highlight_red("No shape type specified"))
        all_points.append(points)
    return canvas


def get_contours_multichannel_old(mask, class_dict, morphology_op=False, hull=False, morphology_kernel_hw=None):
    """Function to get list of contours of mask for different classes
    Args:
        mask : mask with with values 1,2,3... to denote the index of class mask
        class_dict : classes dict with all the contours detected in the mask
        morphology_op = which cv2.morphologyEx operation to apply
        morphology_kernel_hw = kernel for morphology operation
        hull = whether to apply converHull operation
    Returns:
        A dict with all the contours
    """
    contours_dict = {}
    num_classes = len(class_dict)
    for i in range(1, num_classes):
        curr_mask = np.where(mask == i, 255, 0).astype("uint8")
        class_name = class_dict[str(i)]["classname"]
        color = class_dict[str(i)]["color"]
        temp_dict = {"contours": [], "hierarchy": [], "color": color}
        if np.any(curr_mask):
            if morphology_op and morphology_kernel_hw is not None:
                morph_operation = eval(str("cv2." + morphology_op)) # pylint: disable=eval-used
                kernel = np.ones(morphology_kernel_hw, np.uint8)
                curr_mask = cv2.morphologyEx(curr_mask, morph_operation, kernel)
            contours, hierarchy = get_contours(
                curr_mask,
                hull=hull,
                convert_gray=False,
                thresholding=False,
            )
            temp_dict["contours"] = contours
            if len(contours) != len(hierarchy):
                hierarchy = np.squeeze(hierarchy)
            temp_dict["hierarchy"] = hierarchy
        contours_dict[class_name] = temp_dict
    return contours_dict


def get_contours_multichannel(mask, classes, morphology_op=False, hull=False):  ## CHECK ##
    """Function to get list of contours of mask for different classes Attributes"""

    contours_dict = {}
    for ind, classname in enumerate(classes):
        curr_channel = np.where(mask == ind + 1, 255, 0).astype("uint8")
        contours, hierarchy = get_contours(
            curr_channel,
            morphology_op=morphology_op,
            hull=hull,
            convert_gray=False,
            thresholding=False,
        )
        contours_dict[classname] = contours
        # temp_dict["hierarchy"] = hierarchy
    return contours_dict


def get_contour_intersection(cntr1, cntr2):
    """Get intersection between two contours
    Returns the intersection of the input contours
    """
    intersection_cntr_list = []
    cntr_polygon = Polygon(cntr1)
    roi_polygon = Polygon(cntr2)
    roi_polygon = roi_polygon.buffer(0)
    cntr_polygon = cntr_polygon.buffer(0)
    intersection_polygons = roi_polygon.intersection(cntr_polygon)
    if intersection_polygons.geom_type == "MultiPolygon":
        intersection_polygons_ = list(intersection_polygons.geoms)
        for intersection_polygon in intersection_polygons_:
            intersection_cntr = list(intersection_polygon.exterior.coords)
            intersection_cntr_list.append(intersection_cntr)
    elif intersection_polygons.geom_type == "Polygon":
        intersection_cntr_list = [list(intersection_polygons.exterior.coords)]
    intersection_cntrs = []
    for intersection_cntr in intersection_cntr_list:
        cntr = np.array(intersection_cntr)
        if len(cntr) > 1:
            cntr = cntr[:-1] #Removing repeated final point
        intersection_cntrs.append(cntr.tolist())
    return intersection_cntrs


def get_contour_area(cntr):
    """Returns the contour area"""
    area = cv2.contourArea(np.array(cntr))
    return area

def sort_contours_area(contours: Cntr, datalist: Optional[List] = None):
    """Sort contours in descending order of area
    Returns the sorted contours
    """
    sorted_contours = contours
    sorted_datalist = datalist
    if datalist is not None:
        assert len(contours) == len(datalist), "contours and opitonal list must be of same length"
    else:
        datalist = [False] * len(contours)
    if contours:
        sorted_contours, sorted_datalist = zip(*sorted(zip(contours, datalist), key=lambda x: cv2.contourArea(np.array(x[0], dtype=np.int_)), reverse=False))
    return list(sorted_contours), sorted_datalist

def get_xy_loc(points, position="tl", xy_shift=(0, 0)):
    """Find x-y loc based on position given.
    Args:
        position: tl, tr, bl, br, center, ml (middle left)
        pad_list: [top btm left right]
    Returns:
        new x-y loc
    """
    x_shift, y_shift = xy_shift
    x, y, w, h = cv2.boundingRect(points)
    x += x_shift
    y += y_shift
    x = max(0, x)
    y = max(0, y)

    if position == "tl":
        x_loc = x
        y_loc = y
    elif position == "tr":
        x_loc = x + w
        y_loc = y
    elif position == "bl":
        x_loc = x
        y_loc = y + h
    elif position == "br":
        x_loc = x + w
        y_loc = y + h
    elif position == "center":
        x_loc = x + (w / 2)
        y_loc = y + (h / 2)
    elif position == "ml":
        x_loc = x
        y_loc = y + h / 2
    elif position in ["left_aligned", "right_aligned"]:
        x_loc = x_shift
        y_loc = y + h / 2

    return [int(x_loc), int(y_loc)]


def bbox_crop_json(json_dict, bbox):
    """Returns the crop json based on the input box points"""
    x1, y1 = bbox[0]
    x2, y2 = bbox[1]
    json_dict_copy = json_dict.copy()
    crop_json = create_labelme_json()
    crop_shape_list = crop_json["shapes"]
    crop_json["imagePath"] = json_dict_copy["imagePath"]

    roi = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    # roi = [[0, 0], [x2 - x1, 0], [x2 - x1, y2 - y1], [0, y2 - y1]]
    shape_list = json_dict_copy["shapes"]
    for shape in shape_list:
        cntr = shape["points"]
        # cntr_shifted = shift_cntrs([cntr], shift_x=-x1, shift_y=-y1)
        intersection_cntrs = get_contour_intersection(cntr, roi)
        if any(intersection_cntrs):
            for intersection_cntr in intersection_cntrs:
                shape_copy = shape.copy()
                if not is_lab_cntr(intersection_cntr):
                    intersection_cntr = cv2lab(intersection_cntr)
                intersection_cntr = shift_cntrs([intersection_cntr], shift_x=-x1, shift_y=-y1)
                shape_copy["points"] = intersection_cntr[0]
                crop_shape_list.append(shape_copy)
    return crop_json


def get_overlap_area(cntr1, cntr2):
    """Returns the overlap area between two contours"""

    cntr1 = cntr1.astype(np.float32)
    cntr2 = cntr2.astype(np.float32)
    poly1 = Polygon(cntr1)
    poly2 = Polygon(cntr2)
    if not poly1.is_valid:
        poly1 = poly1.buffer(0)
    if not poly2.is_valid:
        poly2 = poly2.buffer(0)
    overlap_area = poly1.intersection(poly2).area
    overlap_area = math.ceil(overlap_area)
    return overlap_area


def make_valid_polygon(polygon):
    """Return a valid shapely polygon"""
    if not polygon.is_valid:
        polygon = polygon.buffer(0)
    return polygon


def check_overlap_height(cntr1, cntr2):
    """Compare y distance (height) of two contours and
    Returns the overlap height
    """
    if not isinstance(cntr1, np.ndarray):
        cntr1 = np.array(cntr1)
    if not isinstance(cntr2, np.ndarray):
        cntr2 = np.array(cntr2)
    x1, y1, w, h = cv2.boundingRect(cntr1)
    x2, y2 = x1 + w, y1 + h
    overlap_height = 0
    x1_, y1_, w, h = cv2.boundingRect(cntr2)
    x2_, y2_ = x1_ + w, y1_ + h
    if y1 < y1_ and y2 < y1_ or y1 > y2_ and y2 > y2_:  # 0
        overlap_height = 0
    elif y1 < y1_ and y2 < y2_:  # 4
        overlap_height = y2 - y1_
    elif y1 > y1_ and y2 > y2_:  # 2
        overlap_height = y2_ - y1
    elif y1 > y1_ and y2 < y2_:  # 3
        overlap_height = y2 - y1
    elif y1_ > y1 and y2 > y2_:  # 5
        overlap_height = y2_ - y1_
    elif y2 == y2_ or y1 == y1_:
        overlap_height = y2 - y1
    return overlap_height


def subtract_contours(cntr1, cntr2):
    """Find difference between  cntr1 and cntr2 using shapely, cntr1 being the smaller
    Retuns the difference between the two contours
    """
    cntr1_polygon = Polygon(cntr1)
    cntr2_polygon = Polygon(cntr2)
    cntr1_polygon = cntr1_polygon.buffer(0)
    cntr2_polygon = cntr2_polygon.buffer(0)
    diff_polygon = cntr1_polygon.difference(cntr2_polygon)
    if diff_polygon.type in ("MultiPolygon", "GeometryCollection"):
        diff_polygon = max(diff_polygon, key=lambda a: a.area)
    diff_cntr = list(diff_polygon.exterior.coords)
    diff_cntr = [[int(x), int(y)] for x, y in diff_cntr]
    return diff_cntr


def check_contour_touches(cntr1, cntr2):
    """Checks if two contours touches at any point
    Returns True if it touches else False
    """
    cntr1_polygon = Polygon(cntr1)
    cntr2_polygon = Polygon(cntr2)
    cntr1_polygon = cntr1_polygon.buffer(0)
    cntr2_polygon = cntr2_polygon.buffer(0)
    if cntr1_polygon.contains(cntr2_polygon) or cntr2_polygon.contains(cntr1_polygon) or cntr1_polygon.intersects(cntr2_polygon):
        return True
    return False


def merge_contours(cntrs_list: List[CntrL]) -> List[CntrL]:
    """Returns the merged contours using shapley"""
    polygons = [Polygon(np.squeeze(cntr).tolist()) for cntr in cntrs_list]
    valid_polygons = []
    for pol in polygons:
        pol_ = make_valid_polygon(pol)
        valid_polygons.append(pol_)
    merged_polygons = unary_union(valid_polygons)
    merged_list = []
    if merged_polygons.geom_type in ("MultiPolygon", "GeometryCollection"):
        merged_polygons = list(merged_polygons.geoms)
        for merged_polygon in merged_polygons:
            intersection_cntr = list(merged_polygon.exterior.coords)
            merged_list.append(intersection_cntr)
    else:
        merged_list = [list(merged_polygons.exterior.coords)]
    return merged_list


def is_lab_cntr(cntr):
    """Returns True is cntr is in labelme support format"""
    if isinstance(cntr, list):
        cntr = np.array(cntr, dtype=object)
    if cntr.ndim == 2:
        return True
    return False


def cv2lab(cntr: CntrC) -> CntrL:
    """Converts cv2 contour [[[x,y]]] to labelme contour [[x,y]]"""
    labelme_cntr = np.squeeze(cntr).tolist()
    return labelme_cntr


def lab2cv(cntr: CntrL) -> CntrC:
    """Converts labelme contour to cv2 contour"""
    cv2_cntr = np.array(cntr).reshape((-1, 1, 2)).astype(np.int32)
    return cv2_cntr


def find_centroid(cntr):
    """Find centroid of given box points.
    Args: cntr
    Returns: Centroid cordinates.
    """
    moments = cv2.moments(np.array(cntr))
    cx = int(moments["m10"] / moments["m00"])
    cy = int(moments["m01"] / moments["m00"])
    return cx, cy

def resize_box(box, x_expn_fact=0.1, y_expn_fact=0):
    """To expand the selected ROI points
    Returns:expanded box
    """
    tl, _, br, bl = box
    width = euclidean(bl, br)
    pad_l, pad_r = int(width * x_expn_fact), int(width * x_expn_fact)
    height = euclidean(tl, bl)
    pad_t, pad_b = int(height * y_expn_fact), int(height * y_expn_fact)
    box_expanded, _, _ = expand_box(box, pad_l=pad_l, pad_r=pad_r, pad_t=pad_t, pad_b=pad_b)
    return box_expanded

def get_box(
    crop_cntr,
    crop_type="fitbox",
    vertical_first: Optional[bool] = True,
):
    """Create box for given contour based on box type
    Returns the box around the contour"""

    assert len(crop_cntr) >= 3, "need atleast three points in crop_cntr"
    crop_cntr = np.array(crop_cntr, dtype=np.float32)

    if crop_type == "trapezoid":
        assert len(crop_cntr) == 4, "trapezoid crop need 4 point roi"
    elif crop_type == "fitbox":
        crop_cntr = getfitbox(crop_cntr, verticalfirst=None)
    elif crop_type == "bbox":
        crop_cntr = getbbox(crop_cntr, verticalfirst=None)
    else:
        raise ValueError(f"crop type {crop_type} not supported")
    box = np.array(crop_cntr, dtype=np.float32)

    # Sorting points for aligning vertically or horizontally
    if vertical_first is not None:
        box = direction_boxsort(box, unit_vec=(0, 1), vertical_sort_first=vertical_first)
    return box

def expand_box(roi, w1=None, h1=None, pad_l=0, pad_r=0, pad_t=0, pad_b=0, expand_dest=True):
    """Function used to expand the selected ROI of Image.
    Args:
        roi : ROI to be expand
        w1,h1 : width and height of destination rectangle
        pad_l (int, optional): Along left, defaults to 0
        pad_r (int, optional): Along right, defaults to 0
        pad_t (int, optional): Along top, defaults to 0
        pad_b (int, optional): Along bottom, defaults to 0
    Returns: src_box expanded, dst_box expanded, forward transform matrix
    """
    roi = np.array(roi, dtype=np.float32)
    pt1, pt2, pt3, _ = roi
    if w1 is None:
        w1 = euclidean(pt1, pt2)
    if h1 is None:
        h1 = euclidean(pt2, pt3)

    dst_points = np.array([[0, 0], [w1, 0], [w1, h1], [0, h1]], dtype=np.float32)

    tr = cv2.getPerspectiveTransform(roi, dst_points)
    tr_inv = np.linalg.inv(tr)  # to map from dst to src
    x1, y1 = 0, 0
    dst_expanded = np.array(
        [
            [x1 - pad_l, y1 - pad_t],
            [x1 + w1 + pad_r, y1 - pad_t],
            [x1 + w1 + pad_r, y1 + h1 + pad_b],
            [x1 - pad_l, y1 + h1 + pad_b],
        ],
        dtype=np.float32,
    )
    src_expanded = transform_contour(np.squeeze(dst_expanded), tr_inv)
    # src_expanded = np.squeeze(src_expanded)
    if expand_dest:
        w1 += pad_l + pad_r
        h1 += pad_t + pad_b
    dst_points = np.array([[0, 0], [w1, 0], [w1, h1], [0, h1]], dtype=np.float32)
    tr = cv2.getPerspectiveTransform(src_expanded, dst_points)
    dst_w_h = (w1, h1)  # exapnded dst width and height
    return src_expanded, dst_w_h, tr

def get_box_dims(box):
    """get h and w of box"""
    pt1, pt2, pt3, _ = box
    width = euclidean(pt1, pt2)
    height = euclidean(pt2, pt3)
    return int(height), int(width)

def split_tiles(box, tiling_info):
    """split tiles
    tiling_info : refer get_tiling_info() in workflow/node_utils"""

    #Set up Initial values
    H, W = icv.transform_utils.get_box_dims(box)
    tiling_loc_list = []
    pad_bottom = 0
    pad_right = 0

    #get tiling params
    tiling_mode = tiling_info.get('tiling_mode')
    tile_x_split = tiling_info.get('tile_x_split')
    tile_y_split = tiling_info.get('tile_y_split')
    overlap_x = tiling_info.get('overlap_x')
    overlap_y = tiling_info.get('overlap_y')
    tile_h = tiling_info.get('tile_h')
    tile_w = tiling_info.get('tile_w')
    vertical_first = tiling_info.get('vertical_first')
    model_h, model_w = tiling_info.get("model_input_HW")
    split_w = (W // tile_x_split) + overlap_x
    split_h = (H // tile_y_split) + overlap_y

    # calculate tile w and tile h
    if tiling_mode == "aspect_ratio_based_tiling":
        if vertical_first:
            tile_w = W
            tile_h = int((W / model_w) * model_h)  # for keeping aspect ratio same as model
        else:
            tile_h = H
            tile_w = int((H / model_h) * model_w)

    if tiling_mode in ("fixed_size_tiling", "aspect_ratio_based_tiling"):
        if W < tile_w:
            pad_right = tile_w - W
            W += pad_right
        w_rem = W % tile_w
        tile_x_split = W // tile_w
        if w_rem > tile_w // 2:
            pad_right += int(tile_w - w_rem)
            W += int(tile_w - w_rem)
            tile_x_split += 1
        elif w_rem > 0:
            split_rem = w_rem // tile_x_split
            tile_w += split_rem
        if H < tile_h:
            pad_bottom = tile_h - H
            H += pad_bottom
        h_rem = H % tile_h
        tile_y_split = H // tile_h
        if h_rem > tile_h // 2:
            pad_bottom += int(tile_h - h_rem)
            H += int(tile_h - h_rem)
            tile_y_split += 1
        elif h_rem > 0:
            split_rem = h_rem // tile_y_split
            tile_h += split_rem

        split_h = tile_h
        split_w = tile_w
        box_expanded, _,_ = icv.transform_utils.expand_box(box, pad_r = pad_right, pad_b = pad_bottom)
        H,W = icv.transform_utils.get_box_dims(box_expanded)

    elif tiling_mode == "fixed_count_tiling":
        split_w = (W // tile_x_split) + overlap_x
        split_h = (H // tile_y_split) + overlap_y

    for i in range(tile_y_split):
        for j in range(tile_x_split):
            x1 = j * split_w
            y1 = i * split_h
            x2 = (j + 1) * split_w
            y2 = (i + 1) * split_h
            if x2 > W:
                x1 = x1 - (tile_x_split) * overlap_x
                x2 = x2 - (tile_x_split) * overlap_x
            if y2 > H:
                y1 = y1 - (tile_y_split) * overlap_y
                y2 = y2 - (tile_y_split) * overlap_y
            tiling_loc_list.append([x1, y1, x2, y2])
            if i == tile_y_split - 1:
                y2 = H
            if j == tile_x_split - 1:
                x2 = W
    return tiling_loc_list


class TestContourUtils(unittest.TestCase):
    """test_contour_utils_options"""

    @classmethod
    def setUpClass(cls):
        cls.pts1_ = [[[1970, 1693], [2161, 1413], [2453, 1452], [2546, 1693], [2227, 1915]]]
        cls.pts2_ = [[[2425, 1304], [2219, 1584], [2340, 1830], [2562, 1872], [2784, 1771]]]

    def test_get_contours(self):
        """test get contours"""
        print("\nTesting the get contours function....")
        mask = np.zeros((224, 224, 3), dtype=np.uint8)
        cv2.line(mask, (0, 0), (100, 100), (0, 255, 0), 50)
        countours, _ = get_contours(
            mask,
            morphology_op="MORPH_DILATE",
            hull=False,
            kernel=None,
            convert_gray=True,
            thresholding=True,
        )
        assert len(countours[0]) == 49, "Contour points count don't match"  ## len of contour points ##

    def test_check_contour_touches(self):
        """test whether 2 contours touch each other"""
        print("\nChecking if the 2 contours touch each other...")
        cntr1 = self.pts1_[0]
        cntr2 = self.pts2_[0]
        touch_flag = check_contour_touches(cntr1, cntr2)
        assert touch_flag is True, "The output does not match"

    def test_check_overlap_height(self):
        """test the overlap height function"""
        print("\nGetting the overlap height of 2 contours....")
        cntr1 = self.pts1_[0]
        cntr2 = self.pts2_[0]
        height = check_overlap_height(cntr1, cntr2)
        assert height == 460, "Height does not match"

    def test_get_xy_loc(self):
        """test get xy position function"""
        print("\nGetting the x-y location based on the input...")
        x, y = get_xy_loc(np.array(self.pts1_), position="tr", xy_shift=(0, 0))
        assert (x, y) == (2547, 1413), "Top right points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="tl", xy_shift=(0, 0))
        assert (x, y) == (1970, 1413), "Top left points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="br", xy_shift=(0, 0))
        assert (x, y) == (2547, 1916), "Bottom right points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="bl", xy_shift=(0, 0))
        assert (x, y) == (1970, 1916), "Bottom left points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="center", xy_shift=(0, 0))
        assert (x, y) == (2258, 1664), "Center points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="ml", xy_shift=(0, 0))
        assert (x, y) == (1970, 1664), "Middle left points dont match"
        x, y = get_xy_loc(np.array(self.pts1_), position="left_aligned", xy_shift=(0, 0))
        assert (x, y) == (0, 1664), "Left alligned points dont match"

    def test_translate_points(self):
        """test translate points function"""
        print("\nTesting translation of points...")
        shifted_points = translate_points(self.pts1_, 10, 10)
        assert shifted_points == [[[1980, 1703], [2171, 1423], [2463, 1462], [2556, 1703], [2237, 1925]]], "Translated points don't match"

    def test_shift_cntrs(self):
        """ "test shift contours function"""
        print("\nTesting shift contours...")
        cntrs_list = [self.pts1_[0], self.pts2_[0]]
        shifted_cntr_list = shift_cntrs(cntrs_list, 10, 10)
        assert shifted_cntr_list == [[[1980, 1703], [2171, 1423], [2463, 1462], [2556, 1703], [2237, 1925]], [[2435, 1314], [2229, 1594], [2350, 1840], [2572, 1882], [2794, 1781]]]

    def test_find_best_match(self):
        """test find best match function"""
        print("\nFinding best match for the given contour...")
        cntr_list = [self.pts1_[0], self.pts2_[0]]
        best_match_index, max_overlap_area = find_best_match(self.pts1_, cntr_list)
        assert (best_match_index, max_overlap_area) == (0, 177949), "The points don't match"

    def test_translate_contour(self):
        """test translate contour function"""
        print("\nTesing translate contour using translation matrix...")
        tr_matrix = get_translation_matrix(10, 10)
        translated_cntr = translate_contour(self.pts1_, tr_matrix)
        assert translated_cntr == [[1980, 1703], [2171, 1423], [2463, 1462], [2556, 1703], [2237, 1925]], "Translated contours don't match"

    def test_sort_contours_area(self):
        """Test sort contours area"""
        print("\nTest sorting with area function...")
        sorted_contours, _ = sort_contours_area([self.pts1_[0], self.pts2_[0]])
        assert sorted_contours == [[[2425, 1304], [2219, 1584], [2340, 1830], [2562, 1872], [2784, 1771]], [[1970, 1693], [2161, 1413], [2453, 1452], [2546, 1693], [2227, 1915]]], "Sorted contours don't match"

    def test_get_contour_area(self):
        """test get contour area"""
        print("\nTesting the get contour area function....")
        area = round(get_contour_area(self.pts1_))
        assert area == 177948, "Area does not match"
        area = round(get_contour_area(self.pts2_))
        assert area == 172416, "Area does not match"


if __name__ == "__main__":
    test_obj = TestContourUtils()
    test_obj.setUpClass()
    test_obj.test_get_contours()
    test_obj.test_check_contour_touches()
    test_obj.test_check_overlap_height()
    test_obj.test_get_xy_loc()
    test_obj.test_translate_points()
    test_obj.test_shift_cntrs()
    test_obj.test_find_best_match()
    test_obj.test_translate_contour()
    test_obj.test_sort_contours_area()
    test_obj.test_get_contour_area()
