import React from 'react';
import { ShieldCheck } from 'lucide-react';

export default function Header({ onNavigate }) {
  const handleNav = (e, sectionId, targetView = 'home') => {
    e.preventDefault();
    if (onNavigate) {
      onNavigate(targetView);
    }
    if (sectionId) {
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };

  return (
    <>
      {/* Main Nav */}
      <header className="w-full bg-white shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <a href="#" onClick={(e) => handleNav(e, null, 'home')} className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <ShieldCheck className="w-8 h-8 text-primary" />
            <span className="font-display text-2xl font-extrabold text-dark tracking-tight uppercase">AutoInspect <span className="text-primary">AI</span></span>
          </a>
          <nav className="hidden md:flex gap-8 text-sm font-display font-semibold uppercase tracking-wider text-dark">
            <a href="#how-it-works" onClick={(e) => handleNav(e, 'how-it-works', 'home')} className="hover:text-primary transition-colors">How it Works</a>
            <a href="#damage-types" onClick={(e) => handleNav(e, 'damage-types', 'home')} className="hover:text-primary transition-colors">Damage Types</a>
            <a href="#help" onClick={(e) => handleNav(e, 'help', 'home')} className="hover:text-primary transition-colors">Help</a>
          </nav>
          <div className="hidden md:block">
            <button 
              onClick={(e) => handleNav(e, null, 'inspect')}
              className="bg-primary hover:bg-primary-hover text-white font-display font-semibold uppercase tracking-wider px-6 py-2 rounded transition-colors"
            >
              Get Estimate
            </button>
          </div>
        </div>
      </header>
    </>
  );
}
