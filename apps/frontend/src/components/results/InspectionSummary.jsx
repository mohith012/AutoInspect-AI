import React from 'react';
import { ShieldAlert, ShieldCheck, Wrench } from 'lucide-react';

export default function InspectionSummary({ vehicle, damages, overallRecommendation }) {
  const getRecStyles = (rec) => {
    if (!rec) return { color: 'text-neutral-600', bg: 'bg-neutral-100', icon: Wrench, border: 'border-neutral-200' };
    const r = rec.toLowerCase();
    if (r === 'repair') return { color: 'text-emerald-700', bg: 'bg-emerald-50', icon: ShieldCheck, border: 'border-emerald-200' };
    if (r === 'replace') return { color: 'text-rose-700', bg: 'bg-rose-50', icon: ShieldAlert, border: 'border-rose-200' };
    return { color: 'text-amber-700', bg: 'bg-amber-50', icon: ShieldAlert, border: 'border-amber-200' };
  };

  const style = getRecStyles(overallRecommendation);
  const Icon = style.icon;

  return (
    <div className="glass-panel p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
      <div>
        <h2 className="font-display text-xl font-bold text-neutral-900 mb-1">
          {vehicle?.make || 'Vehicle'} {vehicle?.model || 'Assessment'}
        </h2>
        <div className="text-sm text-neutral-500 flex gap-2 items-center">
          <span>{vehicle?.year || new Date().getFullYear()}</span>
          <span>&bull;</span>
          <span>{damages?.length || 0} visible damage areas detected</span>
        </div>
      </div>
      
      <div className={`px-5 py-4 rounded-xl border flex items-center gap-4 min-w-[240px] ${style.bg} ${style.border}`}>
        <div className={`p-2 rounded-lg bg-white shadow-sm ${style.color}`}>
          <Icon className="w-6 h-6" />
        </div>
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-neutral-500 mb-0.5">Overall Assessment</p>
          <p className={`text-lg font-bold uppercase tracking-tight ${style.color}`}>
            {overallRecommendation || 'Unknown'}
          </p>
        </div>
      </div>
    </div>
  );
}
