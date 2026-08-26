import React from 'react';
import { ShieldCheck, Phone, Mail, Clock } from 'lucide-react';

export default function Header() {
  return (
    <>
      {/* Top Bar */}
      <div className="bg-dark text-gray-300 py-2 hidden md:block">
        <div className="max-w-7xl mx-auto px-6 flex justify-between items-center text-xs font-display tracking-wide">
          <div className="flex gap-6">
            <span className="flex items-center gap-2"><Phone className="w-3 h-3 text-primary" /> +1 (800) 123-4567</span>
            <span className="flex items-center gap-2"><Mail className="w-3 h-3 text-primary" /> support@autoinspect.ai</span>
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-3 h-3 text-primary" /> Mon - Sat: 8:00 AM - 6:00 PM
          </div>
        </div>
      </div>
      
      {/* Main Nav */}
      <header className="w-full bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <a href="#" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <ShieldCheck className="w-8 h-8 text-primary" />
            <span className="font-display text-2xl font-extrabold text-dark tracking-tight uppercase">AutoInspect <span className="text-primary">AI</span></span>
          </a>
          <nav className="hidden md:flex gap-8 text-sm font-display font-semibold uppercase tracking-wider text-dark">
            <a href="#how-it-works" className="hover:text-primary transition-colors">How it Works</a>
            <a href="#damage-types" className="hover:text-primary transition-colors">Damage Types</a>
            <a href="#help" className="hover:text-primary transition-colors">Help</a>
          </nav>
          <div className="hidden md:block">
            <button className="bg-primary hover:bg-primary-hover text-white font-display font-semibold uppercase tracking-wider px-6 py-2 rounded transition-colors">
              Get Estimate
            </button>
          </div>
        </div>
      </header>
    </>
  );
}
