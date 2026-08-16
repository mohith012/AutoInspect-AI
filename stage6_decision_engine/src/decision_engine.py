import os
import yaml

class DecisionEngine:
    def __init__(self, config_path=None):
        if config_path is None:
            # Default to the config in the project
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(current_dir, "..", "configs", "decision_rules.yaml")
            
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)
            
        self.thresholds = self.config.get("thresholds", {
            "damage_confidence_min": 0.30,
            "part_confidence_min": 0.30,
            "mapping_score_min": 0.30,
            "severity_confidence_min": 0.40
        })
        
        # Build a lookup table from part name to group
        self.part_to_group = {}
        for group_name, group_data in self.config.items():
            if group_name == "thresholds":
                continue
            for part in group_data.get("parts", []):
                self.part_to_group[part] = group_name

    def _generate_reason(self, part, damage, severity, recommendation, rule_used, low_confidence_reason=None):
        if low_confidence_reason:
            return low_confidence_reason
            
        base = f"A {severity} {damage} was detected on the {part}."
        if recommendation == "repair":
            return f"{base} Based on visual assessment, repair may be appropriate. Professional inspection is recommended before repair."
        elif recommendation == "replace":
            return f"{base} Replacement should be considered rather than cosmetic repair. Professional inspection is recommended."
        else:
            return f"{base} The system could not confidently determine repairability. Professional inspection is strictly required."

    def decide_repair_or_replace(self, damage_result):
        """
        Evaluates a single damage result dictionary.
        Expected keys: damaged_part, damage_type, severity, and confidences.
        """
        part = damage_result.get("damaged_part", "uncertain")
        damage = damage_result.get("damage_type", "unknown").replace("maybe ", "")
        severity = damage_result.get("severity", "uncertain")
        
        dam_conf = damage_result.get("damage_confidence")
        part_conf = damage_result.get("part_confidence")
        map_score = damage_result.get("mapping_score")
        sev_conf = damage_result.get("severity_confidence")
        
        # 1. Handle uncertainty or missing inputs
        if part == "uncertain" or severity == "uncertain" or damage == "unknown":
            return {
                "recommendation": "inspect",
                "reason": "The system could not reliably identify the part, damage, or severity. Professional inspection required.",
                "rule_used": "fallback.uncertain_input",
                "requires_professional_inspection": True
            }
            
        # 2. Check confidence thresholds (treat missing confidences as 0.0)
        dam_conf = dam_conf if dam_conf is not None else 0.0
        part_conf = part_conf if part_conf is not None else 0.0
        map_score = map_score if map_score is not None else 0.0
        sev_conf = sev_conf if sev_conf is not None else 0.0
        
        if dam_conf < self.thresholds["damage_confidence_min"]:
             return {
                "recommendation": "inspect",
                "reason": "Low confidence in damage detection.",
                "rule_used": "threshold.damage_confidence",
                "requires_professional_inspection": True
            }
        
        # If mapping score is 0 but part is body, we bypass part confidence check
        if not (part == "body" and map_score == 0.0):
            if part_conf < self.thresholds["part_confidence_min"]:
                 return {
                    "recommendation": "inspect",
                    "reason": "Low confidence in vehicle part detection.",
                    "rule_used": "threshold.part_confidence",
                    "requires_professional_inspection": True
                }
            if map_score < self.thresholds["mapping_score_min"]:
                 return {
                    "recommendation": "inspect",
                    "reason": "Low confidence in mapping the damage to the part.",
                    "rule_used": "threshold.mapping_score",
                    "requires_professional_inspection": True
                }
                
        if sev_conf < self.thresholds["severity_confidence_min"]:
             return {
                "recommendation": "inspect",
                "reason": "Low confidence in severity classification.",
                "rule_used": "threshold.severity_confidence",
                "requires_professional_inspection": True
            }

        # 2.5 Heuristic Filtering (e.g. Reflections)
        if part == "windshield" and damage == "glass_shatter" and dam_conf < 0.85:
            return {
                "recommendation": "inspect",
                "reason": "Low confidence glass shatter detection. This is often caused by glare or tree reflections on the windshield.",
                "rule_used": "heuristic.reflection_filtering",
                "requires_professional_inspection": True
            }

        # 3. Apply Decision Matrix
        group_name = self.part_to_group.get(part)
        
        if not group_name:
            # Unsupported part
            return {
                "recommendation": "inspect",
                "reason": f"No repair rules defined for part: {part}.",
                "rule_used": "fallback.unsupported_part",
                "requires_professional_inspection": True
            }
            
        group_rules = self.config.get(group_name, {})
        damage_rules = group_rules.get(damage)
        
        if not damage_rules:
            # Unsupported damage type for this part
            return {
                "recommendation": "inspect",
                "reason": f"No specific rules defined for {damage} on {part}.",
                "rule_used": f"{group_name}.fallback.unsupported_damage",
                "requires_professional_inspection": True
            }
            
        recommendation = damage_rules.get(severity)
        
        if not recommendation:
            # Unsupported severity
            return {
                "recommendation": "inspect",
                "reason": f"No specific rules defined for {severity} {damage} on {part}.",
                "rule_used": f"{group_name}.{damage}.fallback.unsupported_severity",
                "requires_professional_inspection": True
            }
            
        # Success!
        rule_used = f"{group_name}.{damage}.{severity}"
        reason = self._generate_reason(part, damage, severity, recommendation, rule_used)
        
        return {
            "recommendation": recommendation,
            "reason": reason,
            "rule_used": rule_used,
            "requires_professional_inspection": True
        }

    def evaluate_vehicle(self, damages):
        """
        Evaluates a list of damages and returns the overall vehicle recommendation.
        """
        evaluated_damages = []
        recommendations = set()
        
        for d in damages:
            decision = self.decide_repair_or_replace(d)
            # Merge decision into damage dict
            updated_damage = dict(d)
            updated_damage.update(decision)
            evaluated_damages.append(updated_damage)
            
            recommendations.add(decision["recommendation"])
            
        # Overall logic
        if "replace" in recommendations:
            overall = "replace"
        elif "inspect" in recommendations:
            overall = "inspect"
        elif "repair" in recommendations:
            overall = "repair"
        else:
            overall = "inspect" # fallback
            
        return {
            "damages": evaluated_damages,
            "overall_recommendation": overall
        }
