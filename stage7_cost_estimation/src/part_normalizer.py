class PartNormalizer:
    def __init__(self):
        # Map raw Model 2 outputs to canonical database part names
        self.mapping = {
            "front_bumper": "front_bumper",
            "rear_bumper": "rear_bumper",
            "door": "door",
            "hood": "hood",
            "trunk": "trunk",
            "tailgate": "tailgate",
            "windshield": "windshield",
            "rear_windshield": "rear_windshield",
            "headlight": "headlight",
            "taillight": "taillight",
            "side_mirror": "side_mirror",
            "tire": "tire",
            "body": "body"
        }

    def normalize(self, raw_part_name: str) -> str:
        """
        Normalizes a part name from the detection model to the canonical name in the database.
        """
        if not raw_part_name:
            return "unknown"
        clean_name = raw_part_name.lower().strip()
        return self.mapping.get(clean_name, "unknown")
