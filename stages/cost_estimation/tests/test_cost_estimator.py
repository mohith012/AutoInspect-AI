import unittest
import os
import sys

# Ensure sys.path allows import
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, "..", "src"))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from cost_estimator import CostEstimator

class TestCostEstimator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # We will use an in-memory database for testing or rely on the seeded dev DB
        cls.estimator = CostEstimator()
        
    def test_unknown_vehicle_fallback(self):
        # Should fallback to Generic Hatchback
        vehicle = {"make": "Ferrari", "model": "F40", "year": 1987}
        damage = {"damaged_part": "front_bumper", "severity": "minor", "recommendation": "repair"}
        
        result = self.estimator.estimate_damage_cost(vehicle, damage)
        self.assertEqual(result["price_data_quality"], "medium") # Generic fallback is medium
        self.assertIn("repair_cost", result)
        self.assertGreater(result["total_cost"]["max"], 0)

    def test_hyundai_i20_exact_match(self):
        vehicle = {"make": "Hyundai", "model": "i20", "year": 2022}
        damage = {"damaged_part": "door", "severity": "moderate", "recommendation": "replace"}
        
        result = self.estimator.estimate_damage_cost(vehicle, damage)
        self.assertEqual(result["price_data_quality"], "high")
        self.assertEqual(result["part_cost"]["min"], 8000.0) # Matches seed data
        self.assertEqual(result["part_cost"]["max"], 11000.0)
        self.assertGreater(result["total_cost"]["min"], 8000.0) # Total > Part because of labor

    def test_repair_logic_severity(self):
        vehicle = {"make": "Hyundai", "model": "i20", "year": 2022}
        damage_minor = {"damaged_part": "front_bumper", "severity": "minor", "recommendation": "repair"}
        damage_moderate = {"damaged_part": "front_bumper", "severity": "moderate", "recommendation": "repair"}
        
        res_minor = self.estimator.estimate_damage_cost(vehicle, damage_minor)
        res_mod = self.estimator.estimate_damage_cost(vehicle, damage_moderate)
        
        # Moderate repair should cost more than minor repair
        self.assertGreater(res_mod["repair_cost"]["max"], res_minor["repair_cost"]["max"])

    def test_inspect_recommendation(self):
        vehicle = {"make": "Hyundai", "model": "i20", "year": 2022}
        damage = {"damaged_part": "engine", "severity": "unknown", "recommendation": "inspect"}
        
        result = self.estimator.estimate_damage_cost(vehicle, damage)
        self.assertEqual(result["recommendation"], "inspect")
        self.assertNotIn("total_cost", result)
        self.assertEqual(result["price_data_quality"], "unavailable")

if __name__ == '__main__':
    unittest.main()
