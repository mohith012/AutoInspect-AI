import pytest
from src.bbox_utils import get_center, is_point_in_box, calculate_iou

def test_get_center():
    bbox = [100, 100, 200, 200]
    cx, cy = get_center(bbox)
    assert cx == 150.0
    assert cy == 150.0

def test_is_point_in_box():
    bbox = [100, 100, 200, 200]
    assert is_point_in_box(150, 150, bbox) is True
    assert is_point_in_box(100, 100, bbox) is True  # edge
    assert is_point_in_box(99, 150, bbox) is False
    assert is_point_in_box(150, 201, bbox) is False

def test_calculate_iou_perfect_overlap():
    boxA = [0, 0, 100, 100]
    boxB = [0, 0, 100, 100]
    assert calculate_iou(boxA, boxB) == 1.0

def test_calculate_iou_no_overlap():
    boxA = [0, 0, 10, 10]
    boxB = [20, 20, 30, 30]
    assert calculate_iou(boxA, boxB) == 0.0

def test_calculate_iou_partial_overlap():
    boxA = [0, 0, 100, 100]     # area = 10000
    boxB = [50, 50, 150, 150]   # area = 10000
    # Intersection is [50, 50, 100, 100] = 50x50 = 2500
    # Union = 10000 + 10000 - 2500 = 17500
    # IoU = 2500 / 17500 = 1/7 ≈ 0.1428
    iou = calculate_iou(boxA, boxB)
    assert abs(iou - (2500/17500)) < 0.001
