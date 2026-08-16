import sqlite3
import os
import datetime

class PricingDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(current_dir, "..", "data", "pricing_database", "pricing.db")
        else:
            self.db_path = db_path
            
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._initialize_schema()

    def _initialize_schema(self):
        cursor = self.conn.cursor()
        
        # Vehicles table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make TEXT NOT NULL,
            model TEXT NOT NULL,
            year_start INTEGER,
            year_end INTEGER,
            tier TEXT NOT NULL -- Hatchback, Compact SUV, SUV
        )
        ''')
        
        # Part Prices table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS part_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER,
            part_name TEXT NOT NULL,
            oem_type TEXT NOT NULL,
            price_min REAL NOT NULL,
            price_max REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            source_name TEXT,
            source_url TEXT,
            last_updated TEXT,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles (id)
        )
        ''')
        
        # Labor Rates table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS labor_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_tier TEXT NOT NULL,
            job_type TEXT NOT NULL, -- 'repair_minor', 'repair_moderate', 'replace_panel', 'replace_glass'
            labor_min REAL NOT NULL,
            labor_max REAL NOT NULL,
            currency TEXT DEFAULT 'INR'
        )
        ''')
        
        self.conn.commit()

    def seed_data_if_empty(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        if cursor.fetchone()[0] > 0:
            return # Already seeded
            
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Seed Vehicles (Top 5 in India + i20 + Generic)
        vehicles = [
            ("Maruti Suzuki", "Swift", 2018, 2024, "Hatchback"),       # 1
            ("Hyundai", "i20", 2020, 2024, "Hatchback"),               # 2
            ("Maruti Suzuki", "WagonR", 2019, 2024, "Hatchback"),      # 3
            ("Maruti Suzuki", "Baleno", 2015, 2024, "Hatchback"),      # 4
            ("Tata", "Nexon", 2017, 2024, "Compact SUV"),              # 5
            ("Hyundai", "Creta", 2020, 2024, "SUV"),                   # 6
            ("Generic", "Hatchback", 2010, 2030, "Hatchback"),         # 7 (Fallback)
        ]
        cursor.executemany("INSERT INTO vehicles (make, model, year_start, year_end, tier) VALUES (?, ?, ?, ?, ?)", vehicles)
        
        # Seed Prices
        prices = [
            # 1. Maruti Swift (Hatchback)
            (1, "front_bumper", "OEM", 2500, 3500, "INR", "MGP Catalog Sample", "", now),
            (1, "rear_bumper", "OEM", 2800, 3800, "INR", "MGP Catalog Sample", "", now),
            (1, "headlight", "OEM", 3500, 5000, "INR", "MGP Catalog Sample", "", now),
            (1, "door", "OEM", 6000, 8500, "INR", "MGP Catalog Sample", "", now),
            (1, "windshield", "OEM", 4000, 5500, "INR", "MGP Catalog Sample", "", now),
            
            # 2. Hyundai i20 (Hatchback)
            (2, "front_bumper", "OEM", 3500, 4800, "INR", "Hyundai Mobis Sample", "", now),
            (2, "rear_bumper", "OEM", 3800, 5000, "INR", "Hyundai Mobis Sample", "", now),
            (2, "headlight", "OEM", 6500, 9500, "INR", "Hyundai Mobis Sample", "", now),
            (2, "door", "OEM", 8000, 11000, "INR", "Hyundai Mobis Sample", "", now),
            (2, "windshield", "OEM", 5500, 7500, "INR", "Hyundai Mobis Sample", "", now),
            
            # 3. Maruti WagonR (Hatchback)
            (3, "front_bumper", "OEM", 2200, 3100, "INR", "MGP Catalog Sample", "", now),
            (3, "rear_bumper", "OEM", 2500, 3300, "INR", "MGP Catalog Sample", "", now),
            (3, "headlight", "OEM", 2800, 4000, "INR", "MGP Catalog Sample", "", now),
            (3, "door", "OEM", 5500, 7500, "INR", "MGP Catalog Sample", "", now),
            (3, "windshield", "OEM", 3500, 5000, "INR", "MGP Catalog Sample", "", now),
            
            # 4. Maruti Baleno (Hatchback)
            (4, "front_bumper", "OEM", 2800, 3900, "INR", "Nexa/MGP Sample", "", now),
            (4, "rear_bumper", "OEM", 3000, 4200, "INR", "Nexa/MGP Sample", "", now),
            (4, "headlight", "OEM", 5500, 8000, "INR", "Nexa/MGP Sample", "", now),
            (4, "door", "OEM", 6500, 9000, "INR", "Nexa/MGP Sample", "", now),
            (4, "windshield", "OEM", 4500, 6000, "INR", "Nexa/MGP Sample", "", now),
            
            # 5. Tata Nexon (Compact SUV)
            (5, "front_bumper", "OEM", 4000, 5500, "INR", "Tata Genuine Parts", "", now),
            (5, "rear_bumper", "OEM", 4500, 6000, "INR", "Tata Genuine Parts", "", now),
            (5, "headlight", "OEM", 7500, 11000, "INR", "Tata Genuine Parts", "", now),
            (5, "door", "OEM", 9000, 13000, "INR", "Tata Genuine Parts", "", now),
            (5, "windshield", "OEM", 6500, 8500, "INR", "Tata Genuine Parts", "", now),
            
            # 6. Hyundai Creta (SUV)
            (6, "front_bumper", "OEM", 4500, 6500, "INR", "Hyundai Mobis Sample", "", now),
            (6, "rear_bumper", "OEM", 5000, 7000, "INR", "Hyundai Mobis Sample", "", now),
            (6, "headlight", "OEM", 12000, 18000, "INR", "Hyundai Mobis Sample", "", now), # LEDs are expensive
            (6, "door", "OEM", 11000, 15000, "INR", "Hyundai Mobis Sample", "", now),
            (6, "windshield", "OEM", 7500, 9500, "INR", "Hyundai Mobis Sample", "", now),
            
            # 7. Generic Hatchback (Fallback)
            (7, "front_bumper", "Aftermarket", 2000, 4000, "INR", "Market Average", "", now),
            (7, "rear_bumper", "Aftermarket", 2000, 4000, "INR", "Market Average", "", now),
            (7, "headlight", "Aftermarket", 2500, 6000, "INR", "Market Average", "", now),
            (7, "door", "Aftermarket", 5000, 9000, "INR", "Market Average", "", now),
            (7, "windshield", "Aftermarket", 3500, 6000, "INR", "Market Average", "", now),
            (7, "tire", "Aftermarket", 4000, 7000, "INR", "Market Average", "", now),
        ]
        cursor.executemany('''
            INSERT INTO part_prices 
            (vehicle_id, part_name, oem_type, price_min, price_max, currency, source_name, source_url, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', prices)
        
        # Seed Labor Rates
        labor_rates = [
            # Hatchback
            ("Hatchback", "repair_minor", 800, 1500, "INR"),
            ("Hatchback", "repair_moderate", 1500, 3000, "INR"),
            ("Hatchback", "replace_panel", 1200, 2500, "INR"), 
            ("Hatchback", "replace_glass", 1000, 2000, "INR"),
            ("Hatchback", "replace_simple", 300, 800, "INR"),
            
            # Compact SUV
            ("Compact SUV", "repair_minor", 1000, 1800, "INR"),
            ("Compact SUV", "repair_moderate", 1800, 3500, "INR"),
            ("Compact SUV", "replace_panel", 1500, 3000, "INR"), 
            ("Compact SUV", "replace_glass", 1200, 2500, "INR"),
            ("Compact SUV", "replace_simple", 400, 1000, "INR"),
            
            # SUV
            ("SUV", "repair_minor", 1200, 2200, "INR"),
            ("SUV", "repair_moderate", 2200, 4500, "INR"),
            ("SUV", "replace_panel", 2000, 4000, "INR"), 
            ("SUV", "replace_glass", 1500, 3000, "INR"),
            ("SUV", "replace_simple", 500, 1200, "INR"),
        ]
        cursor.executemany('''
            INSERT INTO labor_rates 
            (vehicle_tier, job_type, labor_min, labor_max, currency)
            VALUES (?, ?, ?, ?, ?)
        ''', labor_rates)
        
        self.conn.commit()

    def get_vehicle_id(self, make: str, model: str, year: int):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT id, tier FROM vehicles 
            WHERE lower(make) = ? AND lower(model) = ? 
            AND (year_start <= ? OR year_start IS NULL) 
            AND (year_end >= ? OR year_end IS NULL)
        ''', (make.lower(), model.lower(), year, year))
        result = cursor.fetchone()
        
        if result:
            return result["id"], result["tier"]
        
        # Fallback to generic
        cursor.execute("SELECT id, tier FROM vehicles WHERE make = 'Generic'")
        fallback = cursor.fetchone()
        return (fallback["id"], fallback["tier"]) if fallback else (None, "Hatchback")

    def get_part_price(self, vehicle_id: int, part_name: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM part_prices 
            WHERE vehicle_id = ? AND part_name = ?
            ORDER BY oem_type DESC LIMIT 1
        ''', (vehicle_id, part_name))
        result = cursor.fetchone()
        
        # If not found for specific vehicle, fallback to generic (id 7)
        if not result and vehicle_id != 7:
            cursor.execute('''
                SELECT * FROM part_prices 
                WHERE vehicle_id = 7 AND part_name = ?
            ''', (part_name,))
            result = cursor.fetchone()
            
        return dict(result) if result else None

    def get_labor_rate(self, vehicle_tier: str, job_type: str):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM labor_rates 
            WHERE vehicle_tier = ? AND job_type = ?
        ''', (vehicle_tier, job_type))
        result = cursor.fetchone()
        
        if not result:
            # Fallback to hatchback labor
            cursor.execute('''
                SELECT * FROM labor_rates 
                WHERE vehicle_tier = 'Hatchback' AND job_type = ?
            ''', (job_type,))
            result = cursor.fetchone()
            
        return dict(result) if result else {"labor_min": 0, "labor_max": 0, "currency": "INR"}

    def close(self):
        self.conn.close()
