import database
import part_normalizer

class CostEstimator:
    def __init__(self, db_path=None):
        self.db = database.PricingDatabase(db_path)
        self.db.seed_data_if_empty()
        self.normalizer = part_normalizer.PartNormalizer()

    def estimate_damage_cost(self, vehicle: dict, damage_result: dict) -> dict:
        """
        Calculates the estimated cost for a single damage result.
        
        vehicle: {"make": "Hyundai", "model": "i20", "year": 2022}
        damage_result: {"damaged_part": "front_bumper", "damage_type": "dent", 
                        "severity": "moderate", "recommendation": "repair"}
        """
        # Default response for inspect or uncertain
        recommendation = damage_result.get("recommendation", "inspect").lower()
        if recommendation not in ["repair", "replace"]:
            return {
                "recommendation": recommendation,
                "price_data_quality": "unavailable",
                "message": "Cost cannot be estimated reliably until the damage is professionally inspected."
            }
            
        # 1. Normalize part and find vehicle ID
        raw_part = damage_result.get("damaged_part", "")
        norm_part = self.normalizer.normalize(raw_part)
        
        make = vehicle.get("make", "Generic")
        model = vehicle.get("model", "Hatchback")
        year = vehicle.get("year", 2022)
        
        vehicle_id, vehicle_tier = self.db.get_vehicle_id(make, model, year)
        if not vehicle_id:
            # Fallback to generic
            vehicle_id = 7
            vehicle_tier = "Hatchback"
            
        # 2. Get Part Price
        part_data = self.db.get_part_price(vehicle_id, norm_part)
        if not part_data:
            return {
                "recommendation": recommendation,
                "price_data_quality": "low",
                "message": f"Insufficient pricing data available for {norm_part}."
            }
            
        # 3. Calculate based on Recommendation
        severity = damage_result.get("severity", "minor").lower()
        
        if recommendation == "replace":
            # Part Cost + Replace Labor
            repair_cost = {"min": 0, "max": 0, "currency": part_data["currency"]}
            part_cost = {
                "min": part_data["price_min"],
                "max": part_data["price_max"],
                "currency": part_data["currency"]
            }
            
            job_type = "replace_glass" if "windshield" in norm_part else "replace_panel"
            if norm_part in ["headlight", "taillight", "side_mirror"]:
                job_type = "replace_simple"
                
            labor_data = self.db.get_labor_rate(vehicle_tier, job_type)
            
        else: # repair
            # Repair logic varies by severity. We don't need a new part.
            part_cost = {"min": 0, "max": 0, "currency": part_data["currency"]}
            
            # Use part value to scale repair cost (expensive parts cost more to repair usually)
            base_val = (part_data["price_min"] + part_data["price_max"]) / 2.0
            
            if severity == "minor":
                r_min, r_max = base_val * 0.1, base_val * 0.2
                job_type = "repair_minor"
            elif severity == "moderate":
                r_min, r_max = base_val * 0.25, base_val * 0.4
                job_type = "repair_moderate"
            else: # severe repair (rare, but handled)
                r_min, r_max = base_val * 0.5, base_val * 0.7
                job_type = "repair_moderate" # Assume heavy labor
                
            repair_cost = {
                "min": round(r_min, 0),
                "max": round(r_max, 0),
                "currency": part_data["currency"]
            }
            labor_data = self.db.get_labor_rate(vehicle_tier, job_type)

        # 4. Total Calculation
        labor_cost = {
            "min": labor_data["labor_min"],
            "max": labor_data["labor_max"],
            "currency": part_data["currency"]
        }
        
        total_min = repair_cost["min"] + part_cost["min"] + labor_cost["min"]
        total_max = repair_cost["max"] + part_cost["max"] + labor_cost["max"]
        
        quality = "high" if vehicle_id != 7 else "medium" # Generic is medium/low

        return {
            "recommendation": recommendation,
            "repair_cost": repair_cost,
            "part_cost": part_cost,
            "labor_cost": labor_cost,
            "total_cost": {
                "min": total_min,
                "max": total_max,
                "currency": part_data["currency"]
            },
            "price_data_quality": quality,
            "source": {
                "name": part_data.get("source_name", "Unknown"),
                "oem_type": part_data.get("oem_type", "Unknown"),
                "last_updated": part_data.get("last_updated", "")
            }
        }
