import React from 'react';
import { Car } from 'lucide-react';

const VEHICLES = [
  { id: 'generic', label: "Generic Hatchback (Fallback)", make: "Generic", model: "Hatchback", year: 2022 },
  { id: 'swift', label: "Maruti Suzuki Swift", make: "Maruti Suzuki", model: "Swift", year: 2022 },
  { id: 'wagonr', label: "Maruti Suzuki WagonR", make: "Maruti Suzuki", model: "WagonR", year: 2022 },
  { id: 'baleno', label: "Maruti Suzuki Baleno", make: "Maruti Suzuki", model: "Baleno", year: 2022 },
  { id: 'nexon', label: "Tata Nexon (Compact SUV)", make: "Tata", model: "Nexon", year: 2022 },
  { id: 'creta', label: "Hyundai Creta (SUV)", make: "Hyundai", model: "Creta", year: 2022 },
  { id: 'i20', label: "Hyundai i20", make: "Hyundai", model: "i20", year: 2022 },
];

export default function VehicleDetailsForm({ selectedVehicle, onVehicleChange }) {
  return (
    <div className="glass-panel p-6 flex flex-col gap-4">
      <div className="flex items-center gap-2 mb-2">
        <Car className="w-5 h-5 text-primary" />
        <h3 className="text-lg font-display font-semibold text-dark tracking-wide uppercase">Vehicle Information</h3>
      </div>
      
      <div className="flex flex-col gap-2">
        <label className="text-sm font-medium text-gray-600 tracking-wide">Select Vehicle Model</label>
        <select 
          className="w-full bg-gray-50 border border-gray-200 text-dark font-sans rounded p-3 outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all cursor-pointer"
          value={selectedVehicle.id}
          onChange={(e) => {
            const vehicle = VEHICLES.find(v => v.id === e.target.value);
            onVehicleChange(vehicle);
          }}
        >
          {VEHICLES.map(v => (
            <option key={v.id} value={v.id}>{v.label}</option>
          ))}
        </select>
        <p className="text-xs text-gray-500 mt-1">
          Used to fetch accurate baseline pricing and labor rates for repairs.
        </p>
      </div>
    </div>
  );
}
