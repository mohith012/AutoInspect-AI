import React from 'react';
import { Check, X, Camera } from 'lucide-react';

export default function PhotoRequirements() {
  return (
    <div className="glass-panel p-6">
      <div className="flex items-center gap-2 mb-4">
        <Camera className="w-5 h-5 text-red-600" />
        <h3 className="text-lg font-semibold text-neutral-900">Photo Requirements</h3>
      </div>
      
      <p className="text-sm text-neutral-600 mb-4">
        For the most accurate AI inspection, please follow these guidelines:
      </p>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
        <div className="flex items-start gap-2 text-neutral-700">
          <div className="mt-0.5 bg-emerald-100 text-emerald-600 p-0.5 rounded-full shrink-0">
            <Check className="w-3 h-3" />
          </div>
          <span>Show the full vehicle</span>
        </div>
        <div className="flex items-start gap-2 text-neutral-700">
          <div className="mt-0.5 bg-emerald-100 text-emerald-600 p-0.5 rounded-full shrink-0">
            <Check className="w-3 h-3" />
          </div>
          <span>Only one vehicle in photo</span>
        </div>
        <div className="flex items-start gap-2 text-neutral-700">
          <div className="mt-0.5 bg-emerald-100 text-emerald-600 p-0.5 rounded-full shrink-0">
            <Check className="w-3 h-3" />
          </div>
          <span>Use good daylight/lighting</span>
        </div>
        <div className="flex items-start gap-2 text-neutral-700">
          <div className="mt-0.5 bg-rose-100 text-rose-600 p-0.5 rounded-full shrink-0">
            <X className="w-3 h-3" />
          </div>
          <span>Avoid strong glare or reflections</span>
        </div>
        <div className="flex items-start gap-2 text-neutral-700">
          <div className="mt-0.5 bg-rose-100 text-rose-600 p-0.5 rounded-full shrink-0">
            <X className="w-3 h-3" />
          </div>
          <span>Avoid heavily obstructed vehicles</span>
        </div>
      </div>
    </div>
  );
}
