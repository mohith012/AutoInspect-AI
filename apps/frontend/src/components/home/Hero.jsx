import React from 'react';
import { ArrowRight, Info } from 'lucide-react';

export default function Hero({ onStart }) {
  return (
    <section className="text-center py-20 px-6 max-w-4xl mx-auto">
      <h1 className="text-4xl md:text-6xl font-bold text-neutral-900 tracking-tight leading-tight mb-6">
        Know What's Damaged. <br className="hidden md:block" />
        <span className="text-red-600">Know What It Could Cost.</span>
      </h1>
      <p className="text-lg text-neutral-600 mb-10 max-w-2xl mx-auto leading-relaxed">
        Upload a photo of your vehicle and AutoInspect AI analyzes visible damage, identifies affected parts, estimates severity, and provides an estimated repair cost.
      </p>
      
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
        <button onClick={onStart} className="btn-primary w-full sm:w-auto text-lg px-8 py-3 rounded-xl shadow-lg shadow-red-600/20 hover:scale-105 transition-transform">
          Inspect My Car <ArrowRight className="w-5 h-5" />
        </button>
        <a href="#how-it-works" className="btn-secondary w-full sm:w-auto text-lg px-8 py-3 rounded-xl hover:scale-105 transition-transform">
          How It Works <Info className="w-5 h-5" />
        </a>
      </div>
    </section>
  );
}
