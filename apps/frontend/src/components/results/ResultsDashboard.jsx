import React from 'react';
import { ArrowLeft, Download } from 'lucide-react';
import InspectionSummary from './InspectionSummary';
import AnnotatedImage from './AnnotatedImage';
import DamageCard from './DamageCard';
import CostBreakdown from './CostBreakdown';

export default function ResultsDashboard({ result, onReset }) {
  if (!result) return null;

  return (
    <div className="max-w-6xl mx-auto px-6 py-12 flex flex-col gap-8">
      
      {/* Top Actions */}
      <div className="flex justify-between items-center">
        <button onClick={onReset} className="btn-secondary text-sm">
          <ArrowLeft className="w-4 h-4" /> Analyze Another Vehicle
        </button>
        <button className="btn-primary text-sm">
          <Download className="w-4 h-4" /> Download Report
        </button>
      </div>

      {/* Hero Summary Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 h-full">
          <InspectionSummary 
            vehicle={result.vehicle} 
            damages={result.damages} 
            overallRecommendation={result.overall_recommendation} 
          />
        </div>
        <div className="lg:col-span-1 h-full">
          <CostBreakdown 
            costData={result.total_cost_estimate} 
            dataQuality={result.price_data_quality} 
          />
        </div>
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Image */}
        <div className="lg:col-span-1 flex flex-col gap-6">
          <h3 className="font-display text-xl font-bold text-neutral-900">Annotated Image</h3>
          <AnnotatedImage imageUrl={result.image_url} />
          
          <div className="glass-panel p-5 bg-neutral-50 mt-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-neutral-500 mb-3">AI Technical Details</h4>
            <div className="space-y-2 text-sm text-neutral-600">
              <div className="flex justify-between border-b border-neutral-200 pb-2">
                <span>Model 1 (Damage)</span>
                <span className="font-medium text-neutral-900">{result.performance['Model 1 (ms)']}ms</span>
              </div>
              <div className="flex justify-between border-b border-neutral-200 pb-2">
                <span>Model 2 (Part)</span>
                <span className="font-medium text-neutral-900">{result.performance['Model 2 (ms)']}ms</span>
              </div>
              <div className="flex justify-between border-b border-neutral-200 pb-2">
                <span>Model 3 (Severity)</span>
                <span className="font-medium text-neutral-900">{result.performance['Model 3 (ms)']}ms</span>
              </div>
              <div className="flex justify-between text-red-600 font-semibold pt-1">
                <span>Total Pipeline</span>
                <span>{result.performance['Total (ms)']}ms</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Damage Cards */}
        <div className="lg:col-span-2">
          <h3 className="font-display text-xl font-bold text-neutral-900 mb-6">Detailed Assessment</h3>
          
          {result.damages?.length === 0 ? (
            <div className="glass-panel p-12 text-center flex flex-col items-center justify-center">
              <div className="w-16 h-16 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mb-4">
                <ShieldCheck className="w-8 h-8" />
              </div>
              <h3 className="font-display text-xl font-bold text-neutral-900 mb-2">No Damage Detected</h3>
              <p className="text-neutral-600 max-w-md mx-auto">
                Our AI models did not detect any visible damage on the supported vehicle parts in this photo.
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {result.damages?.map((damage, idx) => (
                <DamageCard key={idx} damage={damage} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
