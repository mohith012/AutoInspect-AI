import React from 'react';
import { ShieldCheck, ShieldAlert, Wrench, IndianRupee } from 'lucide-react';

export default function DamageCard({ damage }) {
  const isUncertain = damage.damaged_part?.toLowerCase() === 'uncertain';
  
  const getRecStyles = (rec) => {
    if (!rec) return { color: 'text-neutral-600', bg: 'bg-neutral-100', icon: Wrench, border: 'border-neutral-200' };
    const r = rec.toLowerCase();
    if (r === 'repair') return { color: 'text-emerald-700', bg: 'bg-emerald-50', icon: ShieldCheck, border: 'border-emerald-200' };
    if (r === 'replace') return { color: 'text-rose-700', bg: 'bg-rose-50', icon: ShieldAlert, border: 'border-rose-200' };
    return { color: 'text-amber-700', bg: 'bg-amber-50', icon: ShieldAlert, border: 'border-amber-200' };
  };

  const recStyle = getRecStyles(damage.recommendation);
  const RecIcon = recStyle.icon;

  const getSeverityStyle = (sev) => {
    if (!sev) return 'bg-neutral-100 text-neutral-600';
    const s = sev.toLowerCase();
    if (s === 'severe') return 'bg-rose-100 text-rose-700 border-rose-200';
    if (s === 'moderate') return 'bg-amber-100 text-amber-700 border-amber-200';
    return 'bg-emerald-100 text-emerald-700 border-emerald-200';
  };

  return (
    <div className="glass-card flex flex-col h-full">
      <div className="p-5 border-b border-neutral-100">
        <div className="flex justify-between items-start mb-2">
          <div>
            <h3 className={`text-lg font-bold capitalize ${isUncertain ? 'text-amber-600' : 'text-neutral-900'}`}>
              {isUncertain ? 'Part Uncertain' : damage.damaged_part}
            </h3>
            <p className="text-red-600 font-medium capitalize">{damage.damage_type}</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase border ${getSeverityStyle(damage.severity)}`}>
            {damage.severity}
          </span>
        </div>
        
        {isUncertain && (
          <div className="mt-2 text-xs text-amber-700 bg-amber-50 p-2 rounded border border-amber-200">
            Exact vehicle part could not be confidently identified. Professional inspection recommended.
          </div>
        )}
      </div>

      <div className="p-5 flex-1 flex flex-col gap-4 bg-neutral-50/50">
        <div className={`p-4 rounded-xl border flex gap-3 ${recStyle.bg} ${recStyle.border}`}>
          <RecIcon className={`w-5 h-5 shrink-0 ${recStyle.color}`} />
          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-0.5">Recommendation</p>
            <p className={`font-semibold capitalize ${recStyle.color}`}>{damage.recommendation}</p>
            <p className="text-sm text-neutral-600 mt-1 leading-relaxed">{damage.reason}</p>
          </div>
        </div>

        {damage.cost_estimate && damage.cost_estimate.total_cost?.max > 0 ? (
          <div className="bg-white p-4 rounded-xl border border-neutral-200 shadow-sm mt-auto">
            <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3 flex items-center gap-1">
              <IndianRupee className="w-3 h-3" /> Cost Estimate
            </h4>
            <div className="space-y-2 text-sm">
              {damage.cost_estimate.part_cost?.max > 0 && (
                <div className="flex justify-between text-neutral-600">
                  <span>Parts</span>
                  <span className="font-medium text-neutral-900">₹{damage.cost_estimate.part_cost.min.toLocaleString()} – ₹{damage.cost_estimate.part_cost.max.toLocaleString()}</span>
                </div>
              )}
              {damage.cost_estimate.repair_cost?.max > 0 && (
                <div className="flex justify-between text-neutral-600">
                  <span>Repair</span>
                  <span className="font-medium text-neutral-900">₹{damage.cost_estimate.repair_cost.min.toLocaleString()} – ₹{damage.cost_estimate.repair_cost.max.toLocaleString()}</span>
                </div>
              )}
              <div className="flex justify-between text-neutral-600 pb-2 border-b border-neutral-100">
                <span>Labor</span>
                <span className="font-medium text-neutral-900">₹{damage.cost_estimate.labor_cost.min.toLocaleString()} – ₹{damage.cost_estimate.labor_cost.max.toLocaleString()}</span>
              </div>
              <div className="flex justify-between font-bold text-neutral-900 pt-1">
                <span>Total</span>
                <span className="text-red-600">₹{damage.cost_estimate.total_cost.min.toLocaleString()} – ₹{damage.cost_estimate.total_cost.max.toLocaleString()}</span>
              </div>
            </div>
          </div>
        ) : (
          <div className="mt-auto text-xs text-neutral-500 italic p-4 bg-neutral-100 rounded-xl border border-neutral-200">
            {damage.cost_estimate?.message || "Cost estimate unavailable for this damage."}
          </div>
        )}
      </div>
    </div>
  );
}
