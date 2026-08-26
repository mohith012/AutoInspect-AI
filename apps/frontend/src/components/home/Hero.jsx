import React from 'react';
import { ArrowRight, Info } from 'lucide-react';

export default function Hero({ onStart }) {
  return (
    <section className="text-center py-32 px-6 w-full bg-dark relative overflow-hidden">
      {/* Abstract geometric shapes for background interest without images */}
      <div className="absolute top-[-20%] left-[-10%] w-[40%] h-[150%] bg-dark-lighter -rotate-12 z-0"></div>
      <div className="absolute bottom-[-20%] right-[-10%] w-[30%] h-[120%] bg-primary/5 rotate-12 z-0"></div>
      
      <div className="max-w-5xl mx-auto relative z-10">
        <h1 className="text-5xl md:text-7xl font-display font-extrabold text-white tracking-tighter leading-tight mb-8 uppercase">
          Know What's Damaged. <br className="hidden md:block" />
          <span className="text-primary">Know What It Costs.</span>
        </h1>
        <p className="text-lg md:text-xl text-gray-400 mb-12 max-w-3xl mx-auto leading-relaxed">
          Upload a photo of your vehicle and AutoInspect AI analyzes visible damage, identifies affected parts, estimates severity, and provides an estimated repair cost in seconds.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
          <button onClick={onStart} className="btn-primary w-full sm:w-auto shadow-[0_0_20px_rgba(246,33,33,0.4)] hover:shadow-[0_0_30px_rgba(246,33,33,0.6)]">
            Inspect My Car <ArrowRight className="w-5 h-5" />
          </button>
          <a href="#how-it-works" className="btn-secondary w-full sm:w-auto">
            How It Works <Info className="w-5 h-5" />
          </a>
        </div>
      </div>
    </section>
  );
}
