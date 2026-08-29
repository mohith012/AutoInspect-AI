import React, { useState } from 'react';
import { ShieldCheck, ArrowRight, X, Lock, FileText } from 'lucide-react';

export default function Footer({ onNavigate }) {
  const [activeModal, setActiveModal] = useState(null);

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
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <footer className="w-full bg-dark text-gray-400 pt-16 pb-8 border-t-4 border-primary mt-auto relative">
      <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 mb-12">
        {/* About */}
        <div>
          <a href="#" onClick={(e) => handleNav(e, null, 'home')} className="flex items-center gap-2 mb-6">
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
            <li><a href="#" onClick={(e) => handleNav(e, null, 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Home</a></li>
            <li><a href="#how-it-works" onClick={(e) => handleNav(e, 'how-it-works', 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> How It Works</a></li>
            <li><a href="#damage-types" onClick={(e) => handleNav(e, 'damage-types', 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Damage Types</a></li>
            <li><a href="#" onClick={(e) => handleNav(e, null, 'inspect')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Get an Estimate</a></li>
          </ul>
        </div>
        
        {/* Services */}
        <div>
          <h4 className="text-white font-display font-bold uppercase mb-6 relative inline-block after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-8 after:h-0.5 after:bg-primary">Services</h4>
          <ul className="space-y-3 text-sm">
            <li className="flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Damage Detection</li>
            <li className="flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Parts Detection</li>
            <li className="flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Severity Estimation</li>
            <li className="flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Repair Recommendation</li>
            <li className="flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Cost Estimation</li>
          </ul>
        </div>
        
        {/* Resources */}
        <div>
          <h4 className="text-white font-display font-bold uppercase mb-6 relative inline-block after:content-[''] after:absolute after:-bottom-2 after:left-0 after:w-8 after:h-0.5 after:bg-primary">Resources</h4>
          <ul className="space-y-3 text-sm">
            <li><a href="#help" onClick={(e) => handleNav(e, 'help', 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> FAQ</a></li>
            <li><a href="#damage-types" onClick={(e) => handleNav(e, 'damage-types', 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Damage Guide</a></li>
            <li><a href="#how-it-works" onClick={(e) => handleNav(e, 'how-it-works', 'home')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> Repair Guide</a></li>
            <li><a href="#" onClick={(e) => handleNav(e, null, 'inspect')} className="hover:text-primary transition flex items-center gap-2"><ArrowRight className="w-3 h-3 text-primary" /> AI Inspection Guide</a></li>
          </ul>
        </div>
      </div>
      
      <div className="max-w-7xl mx-auto px-6 pt-8 border-t border-gray-800 flex flex-col md:flex-row items-center justify-between gap-4 text-xs">
        <div>
          &copy; {new Date().getFullYear()} AutoInspect AI. All Rights Reserved.
        </div>
        <div className="flex gap-6">
          <button 
            type="button" 
            onClick={() => setActiveModal('privacy')} 
            className="hover:text-primary transition cursor-pointer outline-none"
          >
            Privacy Policy
          </button>
          <button 
            type="button" 
            onClick={() => setActiveModal('terms')} 
            className="hover:text-primary transition cursor-pointer outline-none"
          >
            Terms of Service
          </button>
        </div>
      </div>

      {/* Modal Popup */}
      {activeModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-fade-in">
          <div className="bg-white text-gray-800 rounded-2xl shadow-2xl max-w-2xl w-full max-h-[85vh] flex flex-col overflow-hidden border border-gray-100">
            {/* Modal Header */}
            <div className="px-6 py-5 border-b border-gray-100 flex items-center justify-between bg-gray-50">
              <div className="flex items-center gap-3">
                {activeModal === 'privacy' ? (
                  <div className="p-2 bg-primary/10 rounded-lg text-primary">
                    <Lock className="w-5 h-5" />
                  </div>
                ) : (
                  <div className="p-2 bg-primary/10 rounded-lg text-primary">
                    <FileText className="w-5 h-5" />
                  </div>
                )}
                <h3 className="font-display font-bold text-xl text-dark">
                  {activeModal === 'privacy' ? 'Privacy Policy' : 'Terms of Service'}
                </h3>
              </div>
              <button 
                type="button" 
                onClick={() => setActiveModal(null)} 
                className="text-gray-400 hover:text-dark p-2 rounded-full hover:bg-gray-200 transition cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-4 text-sm leading-relaxed text-gray-600">
              {activeModal === 'privacy' ? (
                <>
                  <p className="font-medium text-gray-800">
                    At <strong>AutoInspect AI</strong>, we prioritize the protection of your data and personal information.
                  </p>
                  
                  <h4 className="font-bold text-dark text-base pt-2">1. Image Data Processing</h4>
                  <p>
                    Photos uploaded for vehicle damage inspection are strictly used to process AI computer vision predictions (damage detection, vehicle part segmentation, and repair estimation).
                  </p>

                  <h4 className="font-bold text-dark text-base pt-2">2. Geolocation & Privacy</h4>
                  <p>
                    When using the Nearby Repair Shops feature, location data is accessed solely through your browser's Geolocation API to fetch nearby service centers via OpenStreetMap. Location data is never stored on our servers.
                  </p>

                  <h4 className="font-bold text-dark text-base pt-2">3. Data Security</h4>
                  <p>
                    All data transmissions between your browser and our API services are encrypted using industry-standard protocols.
                  </p>
                </>
              ) : (
                <>
                  <p className="font-medium text-gray-800">
                    Welcome to <strong>AutoInspect AI</strong>. By accessing our platform, you agree to the following terms:
                  </p>

                  <h4 className="font-bold text-dark text-base pt-2">1. Service Purpose</h4>
                  <p>
                    AutoInspect AI provides automated vehicle damage identification and preliminary cost estimation as an informational tool.
                  </p>

                  <h4 className="font-bold text-dark text-base pt-2">2. Accuracy & Disclaimers</h4>
                  <p>
                    AI predictions and cost estimates are generated using computer vision models and baseline database pricing. Final repair costs may vary depending on local labor rates and detailed hands-on mechanic evaluations.
                  </p>

                  <h4 className="font-bold text-dark text-base pt-2">3. Acceptable Use</h4>
                  <p>
                    Users must only upload clear photos of vehicles they own or have explicit permission to inspect.
                  </p>
                </>
              )}
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex justify-end">
              <button 
                type="button" 
                onClick={() => setActiveModal(null)} 
                className="btn-primary py-2 px-6 text-sm cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </footer>
  );
}
