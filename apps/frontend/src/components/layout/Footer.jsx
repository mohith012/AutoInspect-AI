import React from 'react';

export default function Footer() {
  return (
    <footer className="w-full bg-neutral-50 border-t border-neutral-200 mt-auto">
      <div className="max-w-6xl mx-auto px-6 py-12 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="text-neutral-500 text-sm">
          &copy; {new Date().getFullYear()} AutoInspect AI. Computer Vision Damage Assessment.
        </div>
        <div className="flex gap-4 text-sm text-neutral-500">
          <a href="#" className="hover:text-neutral-900 transition">Privacy</a>
          <a href="#" className="hover:text-neutral-900 transition">Terms</a>
          <a href="#" className="hover:text-neutral-900 transition">Disclaimer</a>
        </div>
      </div>
    </footer>
  );
}
