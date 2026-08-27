import React, { useState } from 'react';
import { HelpCircle, ChevronDown, ChevronUp, ShieldAlert, Sparkles, Wrench } from 'lucide-react';

const FAQS = [
  {
    q: "How accurate is the AI damage inspection?",
    a: "AutoInspect AI uses deep computer vision models trained on thousands of vehicle damage datasets. It detects dents, scratches, cracks, and broken parts with high spatial precision."
  },
  {
    q: "What types of vehicle damage can be evaluated?",
    a: "Our AI can evaluate major and minor dents, paint scratches, bumper damage, windshield/glass cracks, lamp or headlight breakage, and tire damage."
  },
  {
    q: "How is the repair cost estimate calculated?",
    a: "Estimates are calculated by combining detected damage severity with local labor rates and standard replacement part prices across top vehicle makes (e.g. Maruti, Hyundai, Tata)."
  },
  {
    q: "How does the Nearby Repair Shops feature work?",
    a: "Using real-time location data and OpenStreetMap, AutoInspect AI finds local mechanics, tyre centers, and body shops nearest to your current location."
  }
];

export default function HelpFAQ() {
  const [openIndex, setOpenIndex] = useState(0);

  return (
    <section id="help" className="py-20 bg-gray-50 border-t border-neutral-200">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-12">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-red-100 text-primary text-xs font-semibold uppercase tracking-wider rounded-full mb-3">
            <HelpCircle className="w-4 h-4" /> Frequently Asked Questions
          </span>
          <h2 className="font-display text-3xl md:text-4xl font-extrabold text-neutral-900">
            Need Help with <span className="text-primary">AutoInspect AI</span>?
          </h2>
          <p className="mt-3 text-neutral-600 max-w-2xl mx-auto">
            Find answers to common questions about our AI damage detection pipeline, cost estimation, and nearby service centers.
          </p>
        </div>

        <div className="space-y-4">
          {FAQS.map((faq, idx) => (
            <div key={idx} className="bg-white border border-neutral-200 rounded-xl overflow-hidden shadow-sm transition">
              <button
                onClick={() => setOpenIndex(openIndex === idx ? null : idx)}
                className="w-full px-6 py-5 flex items-center justify-between text-left font-display font-semibold text-neutral-900 hover:text-primary transition"
              >
                <span className="text-lg">{faq.q}</span>
                {openIndex === idx ? (
                  <ChevronUp className="w-5 h-5 text-primary shrink-0" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-neutral-400 shrink-0" />
                )}
              </button>
              {openIndex === idx && (
                <div className="px-6 pb-6 text-neutral-600 text-sm leading-relaxed border-t border-neutral-100 pt-4">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
