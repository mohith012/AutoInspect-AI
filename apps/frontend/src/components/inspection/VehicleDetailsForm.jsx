import React, { useState, useRef, useEffect } from 'react';
import { Car, ChevronDown, Check } from 'lucide-react';

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
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="glass-panel !overflow-visible p-6 flex flex-col gap-4">
      <div className="flex items-center gap-2 mb-2">
        <Car className="w-5 h-5 text-primary" />
        <h3 className="text-lg font-display font-semibold text-dark tracking-wide uppercase">Vehicle Information</h3>
      </div>
      
      <div className="flex flex-col gap-2 relative" ref={dropdownRef}>
        <label className="text-sm font-medium text-gray-600 tracking-wide">Select Vehicle Model</label>
        
        {/* Custom Dropdown Trigger */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className="w-full flex items-center justify-between bg-white border border-gray-200 text-dark font-sans rounded-xl p-3.5 shadow-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all text-left cursor-pointer"
        >
          <span className="font-semibold text-sm">{selectedVehicle.label}</span>
          <ChevronDown className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Custom Dropdown List */}
        {isOpen && (
          <div className="absolute top-[82px] left-0 z-50 w-full bg-white border border-gray-100 rounded-xl shadow-xl py-1.5 max-h-64 overflow-y-auto">
            {VEHICLES.map((v) => {
              const isSelected = v.id === selectedVehicle.id;
              return (
                <button
                  key={v.id}
                  type="button"
                  onClick={() => {
                    onVehicleChange(v);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-center justify-between px-4 py-3 text-left transition-colors ${
                    isSelected 
                      ? 'bg-primary/5 text-primary font-semibold' 
                      : 'hover:bg-gray-50 text-gray-700'
                  }`}
                >
                  <div className="flex flex-col">
                    <span className="text-sm">{v.label}</span>
                    <span className={`text-[10px] uppercase tracking-wider ${isSelected ? 'text-primary/70' : 'text-gray-400'}`}>
                      {v.make} • {v.model}
                    </span>
                  </div>
                  {isSelected && <Check className="w-4 h-4 text-primary" />}
                </button>
              );
            })}
          </div>
        )}

        <p className="text-xs text-gray-500 mt-1">
          Used to fetch accurate India-specific baseline pricing and labor rates for repairs.
        </p>
      </div>
    </div>
  );
}
