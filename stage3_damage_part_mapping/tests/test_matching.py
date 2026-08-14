import pytest
from src.matcher import match_damages_to_parts

def test_perfect_match():
    damages = [{"damage": "dent", "confidence": 0.9, "bbox": [120, 120, 180, 180]}]
    parts = [{"part": "door", "confidence": 0.95, "bbox": [100, 100, 200, 200]}]
    
    res = match_damages_to_parts(damages, parts)
    assert len(res) == 1
    assert res[0]['damaged_part'] == 'door'
    assert res[0]['mapping_score'] > 0.6  # Center is inside + IoU

def test_no_parts_detected():
    damages = [{"damage": "scratch", "confidence": 0.8, "bbox": [10, 10, 20, 20]}]
    assert len(res) == 1
    assert res[0]['damaged_part'] == 'body'
    assert res[0]['mapping_score'] == 0.0

def test_multiple_damages_independent_mapping():
    damages = [
        {"damage": "dent", "confidence": 0.9, "bbox": [120, 120, 180, 180]},   # inside door
        {"damage": "crack", "confidence": 0.8, "bbox": [320, 320, 380, 380]}   # inside bumper
    ]
    parts = [
        {"part": "door", "confidence": 0.95, "bbox": [100, 100, 200, 200]},
        {"part": "front_bumper", "confidence": 0.92, "bbox": [300, 300, 400, 400]}
    ]
    
    res = match_damages_to_parts(damages, parts)
    assert len(res) == 2
    
    # Check dent
    dent_res = next(r for r in res if r['damage'] == 'dent')
    assert dent_res['damaged_part'] == 'door'
    
    # Check crack
    crack_res = next(r for r in res if r['damage'] == 'crack')
    assert crack_res['damaged_part'] == 'front_bumper'

def test_ambiguous_overlap():
    # Damage exactly on the border of two parts
    damages = [{"damage": "scratch", "confidence": 0.9, "bbox": [140, 140, 160, 160]}]
    parts = [
        {"part": "door", "confidence": 0.9, "bbox": [100, 100, 160, 200]},
        {"part": "fender", "confidence": 0.9, "bbox": [140, 100, 200, 200]}
    ]
    # Under the new explicit logic, it just takes the first/highest candidate rather than refusing.
    res = match_damages_to_parts(damages, parts)
    assert len(res) == 1
    assert res[0]['damaged_part'] in ['door', 'fender']
