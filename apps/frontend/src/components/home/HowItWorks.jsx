import React from 'react';
import { Upload, Scan, CarFront, AlertCircle, Wrench, IndianRupee, ArrowDown } from 'lucide-react';

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
    <section id="how-it-works" className="py-20 bg-white border-t border-neutral-200">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="font-display text-3xl font-bold text-neutral-900 mb-4">How AutoInspect AI Works</h2>
          <p className="text-neutral-600 max-w-2xl mx-auto">
            Our pipeline combines multiple computer vision models to provide a comprehensive analysis in seconds.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 relative">
          {STEPS.map((step, idx) => (
            <div key={idx} className="relative glass-panel p-6 flex flex-col h-full group hover:-tranneutral-y-1 hover:shadow-md hover:border-red-200 transition-all cursor-default">
              <div className="text-5xl font-black text-neutral-100 absolute top-4 right-4 z-0 pointer-events-none transition-colors group-hover:text-red-50">
                {step.num}
              </div>
              <div className="relative z-10 flex flex-col h-full">
                <div className="w-12 h-12 rounded-xl bg-red-50 text-red-600 flex items-center justify-center mb-4">
                  <step.icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-neutral-900 mb-2">{step.title}</h3>
                <p className="text-sm text-neutral-600">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
