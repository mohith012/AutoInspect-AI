import React, { useState, useEffect } from 'react';
import { CheckCircle2, CircleDashed, Circle } from 'lucide-react';

export default function LoadingProgress({ steps }) {
  // steps is an array of objects: { id: string, label: string, status: 'pending' | 'active' | 'completed' }
  return (
    <div className="w-full max-w-md mx-auto p-8 glass-panel">
      <h3 className="text-xl font-semibold mb-6 text-center text-neutral-900">Analyzing your vehicle</h3>
      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-center gap-3">
            {step.status === 'completed' && <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />}
            {step.status === 'active' && <CircleDashed className="w-5 h-5 text-red-500 animate-spin shrink-0" />}
            {step.status === 'pending' && <Circle className="w-5 h-5 text-neutral-300 shrink-0" />}
            <span className={`text-sm font-medium ${
              step.status === 'completed' ? 'text-neutral-900' : 
              step.status === 'active' ? 'text-red-600' : 'text-neutral-400'
            }`}>
              {step.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
