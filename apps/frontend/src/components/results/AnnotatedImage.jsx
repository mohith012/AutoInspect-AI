import React from 'react';
import { ZoomIn } from 'lucide-react';

export default function AnnotatedImage({ imageUrl }) {
  return (
    <div className="glass-panel p-2 flex flex-col relative group">
      <div className="bg-neutral-100 rounded-xl overflow-hidden relative">
        <img 
          src={`http://localhost:8000${imageUrl}`} 
          alt="AI Annotated Vehicle" 
          className="w-full h-auto max-h-[500px] object-contain"
        />
        <div className="absolute bottom-4 right-4 bg-white/90 backdrop-blur px-3 py-1.5 rounded-lg shadow-sm border border-neutral-200 flex items-center gap-2 text-xs font-medium text-neutral-700 opacity-0 group-hover:opacity-100 transition-opacity">
          <ZoomIn className="w-3.5 h-3.5" /> Hover to inspect
        </div>
      </div>
    </div>
  );
}
