import React from 'react';
import { Target, Shield } from 'lucide-react';

const DAMAGES = ['Dent', 'Scratch', 'Crack', 'Glass shatter', 'Lamp broken', 'Tire flat'];
const PARTS = ['Front bumper', 'Rear bumper', 'Door', 'Hood', 'Windshield', 'Headlight', 'Tire', 'Body'];

export default function WhatWeDetect() {
  return (
    <section id="damage-types" className="py-24 bg-dark-lighter text-white relative">
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-16">
          <h2 className="section-title-center text-white">What We Detect</h2>
          <p className="text-gray-400 max-w-2xl mx-auto mt-6">
            Our models are trained on thousands of vehicle damage images to recognize common damage types and map them to their corresponding vehicle parts.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="bg-dark p-10 border border-gray-800 rounded-lg shadow-xl relative overflow-hidden group hover:border-primary transition-colors duration-300">
            <div className="absolute top-0 right-0 w-24 h-24 bg-primary/10 rounded-bl-full -mr-4 -mt-4 transition-transform duration-500 group-hover:scale-110"></div>
            <div className="flex items-center gap-4 mb-8 relative z-10">
              <div className="p-3 bg-primary/20 text-primary rounded-br-xl">
                <Target className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-display font-bold uppercase tracking-wider text-white">Damage Types</h3>
            </div>
            <div className="flex flex-wrap gap-3 relative z-10">
              {DAMAGES.map(d => (
                <span key={d} className="px-5 py-2 bg-dark-lighter border border-gray-700 text-gray-300 rounded font-display tracking-wide shadow-sm hover:bg-primary hover:text-white hover:border-primary cursor-default transition-colors duration-300">
                  {d}
                </span>
              ))}
            </div>
          </div>
          
          <div className="bg-dark p-10 border border-gray-800 rounded-lg shadow-xl relative overflow-hidden group hover:border-primary transition-colors duration-300">
             <div className="absolute top-0 right-0 w-24 h-24 bg-primary/10 rounded-bl-full -mr-4 -mt-4 transition-transform duration-500 group-hover:scale-110"></div>
            <div className="flex items-center gap-4 mb-8 relative z-10">
              <div className="p-3 bg-primary/20 text-primary rounded-br-xl">
                <Shield className="w-8 h-8" />
              </div>
              <h3 className="text-2xl font-display font-bold uppercase tracking-wider text-white">Vehicle Parts</h3>
            </div>
            <div className="flex flex-wrap gap-3 relative z-10">
              {PARTS.map(p => (
                <span key={p} className="px-5 py-2 bg-dark-lighter border border-gray-700 text-gray-300 rounded font-display tracking-wide shadow-sm hover:bg-primary hover:text-white hover:border-primary cursor-default transition-colors duration-300">
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
