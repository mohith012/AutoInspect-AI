import React from 'react';
import { IndianRupee, AlertCircle } from 'lucide-react';

export default function CostBreakdown({ costData, dataQuality }) {
  if (!costData || costData.max === 0 || dataQuality === 'unavailable') {
    return (
      <div className="glass-panel p-6 bg-neutral-50 border-dashed">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-neutral-500 mb-2">Estimated Repair Cost</h3>
        <div className="flex items-center gap-3 text-amber-700 bg-amber-50 p-4 rounded-lg border border-amber-200">
          <AlertCircle className="w-5 h-5 shrink-0" />
          <p className="text-sm">Cost estimate unavailable. We do not have reliable pricing data for this vehicle/part combination.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-panel p-6 bg-gradient-to-br from-red-600 to-indigo-700 text-white shadow-xl shadow-red-900/10">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h3 className="text-sm font-bold uppercase tracking-wider text-red-200 mb-1">Estimated Repair Cost</h3>
          <div className="flex items-baseline gap-1">
            <span className="text-4xl font-black tracking-tight">₹{costData.min.toLocaleString()}</span>
            <span className="text-xl text-red-200 font-medium"> – ₹{costData.max.toLocaleString()}</span>
          </div>
        </div>
        <div className="p-2 bg-white/10 rounded-lg">
          <IndianRupee className="w-6 h-6 text-red-100" />
        </div>
      </div>
      
      <p className="text-xs text-red-200/80 mt-4 pt-4 border-t border-red-500/30">
        Estimated cost — actual workshop prices may vary based on location and labor rates.
        Data Quality: {dataQuality?.toUpperCase() || 'STANDARD'}
      </p>
    </div>
  );
}
