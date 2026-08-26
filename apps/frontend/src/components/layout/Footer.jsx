import React from 'react';
import { ShieldCheck, MapPin, Phone, Mail, ArrowRight } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full bg-dark text-gray-400 pt-16 pb-8 border-t-4 border-primary mt-auto">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        {/* About */}
        <div>
          <a href="#" className="flex items-center gap-2 mb-6">
            <ShieldCheck className="w-8 h-8 text-primary" />
            <span className="font-display text-2xl font-extrabold text-white tracking-tight uppercase">AutoInspect <span className="text-primary">AI</span></span>
          </a>
          <p className="text-sm leading-relaxed mb-6">
            Advanced computer vision technology to assess vehicle damage, identify affected parts, and estimate repair costs instantly.
          </p>
        </div>
        
        {/* Quick Links */}
        <div>
          <h4 className="text-white font-display font-bold uppercase mb-6 relative inline-block after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-8 after:h-0.5 after:bg-primary">Quick Links</h4>
          <ul className="space-y-3 text-sm">
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Home</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> How It Works</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Damage Types</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Get an Estimate</a></li>
          </ul>
        </div>
        
        {/* Services */}
        <div>
          <h4 className="text-white font-display font-bold uppercase mb-6 relative inline-block after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-8 after:h-0.5 after:bg-primary">Services</h4>
          <ul className="space-y-3 text-sm">
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Dent Detection</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Scratch Analysis</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Glass Damage</a></li>
            <li><a href="#" className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Cost Estimation</a></li>
          </ul>
        </div>
        
        {/* Contact */}
        <div>
          <h4 className="text-white font-display font-bold uppercase mb-6 relative inline-block after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-8 after:h-0.5 after:bg-primary">Contact Us</h4>
          <ul className="space-y-4 text-sm">
            <li className="flex items-start gap-3">
              <MapPin className="w-5 h-5 text-primary shrink-0" />
              <span>123 Innovation Drive, Tech Park, AI City 10001</span>
            </li>
            <li className="flex items-center gap-3">
              <Phone className="w-5 h-5 text-primary shrink-0" />
              <span>+1 (800) 123-4567</span>
            </li>
            <li className="flex items-center gap-3">
              <Mail className="w-5 h-5 text-primary shrink-0" />
              <span>support@autoinspect.ai</span>
            </li>
          </ul>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-6 pt-8 border-t border-gray-800 flex flex-col md:flex-row items-center justify-between gap-4 text-xs">
        <div>
          &copy; {new Date().getFullYear()} AutoInspect AI. All Rights Reserved.
        </div>
        <div className="flex gap-6">
          <a href="#" className="hover:text-primary transition">Privacy Policy</a>
          <a href="#" className="hover:text-primary transition">Terms of Service</a>
        </div>
      </div>
    </footer>
  );
}
