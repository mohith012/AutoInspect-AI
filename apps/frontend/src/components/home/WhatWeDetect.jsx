import React from 'react';
import { Target } from 'lucide-react';

const DAMAGES = ['Dent', 'Scratch', 'Crack', 'Glass shatter', 'Lamp broken', 'Tire flat'];
const PARTS = ['Front bumper', 'Rear bumper', 'Door', 'Hood', 'Windshield', 'Headlight', 'Tire', 'Body'];

export default function WhatWeDetect() {
  return (
    <section id="damage-types" className="py-20 bg-neutral-50">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-12">
          <h2 className="font-display text-3xl font-bold text-neutral-900 mb-4">What We Detect</h2>
          <p className="text-neutral-600 max-w-2xl mx-auto">
            Our models are trained on thousands of vehicle damage images to recognize common damage types and map them to their corresponding vehicle parts.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="glass-panel p-8">
            <div className="flex items-center gap-3 mb-6">
              <Target className="w-6 h-6 text-red-600" />
              <h3 className="text-xl font-semibold text-neutral-900">Damage Types</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {DAMAGES.map(d => (
                <span key={d} className="px-4 py-2 bg-white border border-neutral-200 text-neutral-700 rounded-full text-sm font-medium shadow-sm hover:bg-red-50 hover:text-red-700 hover:border-red-200 cursor-default transition-colors">
                  {d}
                </span>
              ))}
            </div>
          </div>
          
          <div className="glass-panel p-8">
            <div className="flex items-center gap-3 mb-6">
              <Target className="w-6 h-6 text-red-600" />
              <h3 className="text-xl font-semibold text-neutral-900">Vehicle Parts</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {PARTS.map(p => (
                <span key={p} className="px-4 py-2 bg-white border border-neutral-200 text-neutral-700 rounded-full text-sm font-medium shadow-sm hover:bg-red-50 hover:text-red-700 hover:border-red-200 cursor-default transition-colors">
                  {p}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
