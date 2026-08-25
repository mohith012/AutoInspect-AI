import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function Header() {
  return (
    <header className="w-full bg-white border-b border-neutral-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <a href="#" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
          <ShieldCheck className="w-7 h-7 text-red-600" />
          <span className="font-display text-xl font-bold text-neutral-900 tracking-tight">AutoInspect AI</span>
        </a>
        <nav className="hidden md:flex gap-8 text-sm font-medium text-neutral-600">
          <a href="#how-it-works" className="hover:text-red-600 hover:bg-red-50 px-3 py-2 rounded-lg transition-all">How it Works</a>
          <a href="#damage-types" className="hover:text-red-600 hover:bg-red-50 px-3 py-2 rounded-lg transition-all">Damage Types</a>
          <a href="#help" className="hover:text-red-600 hover:bg-red-50 px-3 py-2 rounded-lg transition-all">Help</a>
        </nav>
      </div>
    </header>
  );
}
