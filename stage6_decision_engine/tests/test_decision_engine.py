import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
stage6_path = os.path.join(project_root, "stage6_decision_engine", "src")
if stage6_path not in sys.path:
    sys.path.insert(0, stage6_path)

from decision_engine import DecisionEngine

class TestDecisionEngine(unittest.TestCase):
    def setUp(self):
        self.engine = DecisionEngine()
        
    def _create_payload(self, part, damage, severity, dam_conf=0.9, part_conf=0.9, map_score=0.9, sev_conf=0.9):
        return {
            "damaged_part": part,
            "damage_type": damage,
            "severity": severity,
            "damage_confidence": dam_conf,
            "part_confidence": part_conf,
            "mapping_score": map_score,
            "severity_confidence": sev_conf
        }

    def test_1_minor_bumper_dent(self):
        payload = self._create_payload("front_bumper", "dent", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "repair")
        
    def test_2_moderate_bumper_dent(self):
        payload = self._create_payload("rear_bumper", "dent", "moderate")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "repair")

    def test_3_severe_bumper_dent(self):
        payload = self._create_payload("front_bumper", "dent", "severe")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_4_severe_bumper_crack(self):
        payload = self._create_payload("front_bumper", "crack", "severe")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "replace")
        
    def test_5_windshield_crack(self):
        payload = self._create_payload("windshield", "crack", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")
        
        payload2 = self._create_payload("windshield", "crack", "moderate")
        res2 = self.engine.decide_repair_or_replace(payload2)
        self.assertEqual(res2["recommendation"], "replace")

    def test_6_broken_lamp(self):
        payload = self._create_payload("headlight", "lamp_broken", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "replace")

    def test_7_tire_damage(self):
        payload = self._create_payload("tire", "tire_flat", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_8_unknown_part(self):
        payload = self._create_payload("uncertain", "dent", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_9_unknown_severity(self):
        payload = self._create_payload("front_bumper", "dent", "uncertain")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")
        
    def test_10_low_model_1_conf(self):
        payload = self._create_payload("front_bumper", "dent", "minor", dam_conf=0.1)
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_11_low_model_2_conf(self):
        payload = self._create_payload("front_bumper", "dent", "minor", part_conf=0.1)
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_12_low_mapping_score(self):
        payload = self._create_payload("front_bumper", "dent", "minor", map_score=0.1)
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")
        
    def test_13_low_model_3_conf(self):
        payload = self._create_payload("front_bumper", "dent", "minor", sev_conf=0.1)
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_14_15_multiple_damages_and_conflicts(self):
        damages = [
            self._create_payload("front_bumper", "dent", "minor"), # repair
            self._create_payload("headlight", "lamp_broken", "severe") # replace
        ]
        res = self.engine.evaluate_vehicle(damages)
        self.assertEqual(res["overall_recommendation"], "replace")
        self.assertEqual(res["damages"][0]["recommendation"], "repair")
        self.assertEqual(res["damages"][1]["recommendation"], "replace")
        
    def test_16_missing_input_fields(self):
        res = self.engine.decide_repair_or_replace({})
        self.assertEqual(res["recommendation"], "inspect")

    def test_17_unsupported_part(self):
        payload = self._create_payload("exhaust_pipe", "dent", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

    def test_18_unsupported_damage_type(self):
        payload = self._create_payload("front_bumper", "acid_burn", "minor")
        res = self.engine.decide_repair_or_replace(payload)
        self.assertEqual(res["recommendation"], "inspect")

if __name__ == "__main__":
    unittest.main()
