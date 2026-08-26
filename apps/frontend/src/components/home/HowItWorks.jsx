import React from 'react';
import { Upload, Scan, CarFront, AlertCircle, Wrench, IndianRupee } from 'lucide-react';

const STEPS = [
  { num: '01', title: 'Upload Photo', icon: Upload, desc: 'Upload a clear photo of the damaged vehicle.' },
  { num: '02', title: 'Detect Damage', icon: Scan, desc: 'AI highlights visible damage areas.' },
  { num: '03', title: 'Identify Parts', icon: CarFront, desc: 'Maps damage to specific vehicle parts.' },
  { num: '04', title: 'Estimate Severity', icon: AlertCircle, desc: 'Categorizes damage as minor, moderate, or severe.' },
  { num: '05', title: 'Recommend Action', icon: Wrench, desc: 'Suggests Repair, Replace, or Inspect.' },
  { num: '06', title: 'Estimate Cost', icon: IndianRupee, desc: 'Calculates approximate part and labor costs.' },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="section-title-center">How AutoInspect AI Works</h2>
          <p className="text-gray-500 max-w-2xl mx-auto mt-6">
            Our pipeline combines multiple computer vision models to provide a comprehensive analysis in seconds.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 relative">
          {STEPS.map((step, idx) => (
            <div key={idx} className="glass-card p-8 flex flex-col h-full group cursor-default bg-white">
              <div className="text-6xl font-display font-black text-gray-100 absolute top-4 right-4 z-0 pointer-events-none transition-colors duration-300 group-hover:text-primary/10">
                {step.num}
              </div>
              <div className="relative z-10 flex flex-col h-full">
                <div className="w-14 h-14 bg-gray-100 text-primary flex items-center justify-center mb-6 transition-colors duration-300 group-hover:bg-primary group-hover:text-white rounded-br-2xl">
                  <step.icon className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-display font-bold text-dark uppercase tracking-wide mb-3">{step.title}</h3>
                <p className="text-gray-500 leading-relaxed">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
