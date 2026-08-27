import React, { useState, useEffect } from 'react';
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';
import Hero from './components/home/Hero';
import HowItWorks from './components/home/HowItWorks';
import WhatWeDetect from './components/home/WhatWeDetect';
import HelpFAQ from './components/home/HelpFAQ';
import VehicleDetailsForm from './components/inspection/VehicleDetailsForm';
import PhotoRequirements from './components/inspection/PhotoRequirements';
import UploadArea from './components/inspection/UploadArea';
import LoadingProgress from './components/shared/LoadingProgress';
import ResultsDashboard from './components/results/ResultsDashboard';

const VEHICLES = [
  { id: 'generic', label: "Generic Hatchback (Fallback)", make: "Generic", model: "Hatchback", year: 2022 },
  { id: 'swift', label: "Maruti Suzuki Swift", make: "Maruti Suzuki", model: "Swift", year: 2022 },
  { id: 'wagonr', label: "Maruti Suzuki WagonR", make: "Maruti Suzuki", model: "WagonR", year: 2022 },
  { id: 'baleno', label: "Maruti Suzuki Baleno", make: "Maruti Suzuki", model: "Baleno", year: 2022 },
  { id: 'nexon', label: "Tata Nexon (Compact SUV)", make: "Tata", model: "Nexon", year: 2022 },
  { id: 'creta', label: "Hyundai Creta (SUV)", make: "Hyundai", model: "Creta", year: 2022 },
  { id: 'i20', label: "Hyundai i20", make: "Hyundai", model: "i20", year: 2022 },
];

export default function App() {
  const [view, setView] = useState('home'); // 'home', 'inspect', 'loading', 'results'
  const [selectedVehicle, setSelectedVehicle] = useState(VEHICLES[0]);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loadingSteps, setLoadingSteps] = useState([
    { id: 'upload', label: 'Image received', status: 'pending' },
    { id: 'model1', label: 'Detecting visible damage', status: 'pending' },
    { id: 'model2', label: 'Identifying affected parts', status: 'pending' },
    { id: 'severity', label: 'Estimating severity', status: 'pending' },
    { id: 'cost', label: 'Calculating repair estimate', status: 'pending' },
  ]);

  // Handle paste events globally for the inspection view
  useEffect(() => {
    if (view !== 'inspect') return;
    const handlePaste = (e) => {
      const items = e.clipboardData?.items;
      if (!items) return;
      for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
          const blob = items[i].getAsFile();
          handleFileSelection(blob);
          break;
        }
      }
    };
    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, [view]);

  const handleFileSelection = (selected) => {
    if (selected && selected.type.startsWith('image/')) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setError(null);
    } else {
      setFile(null);
      setPreview(null);
    }
  };

  const simulateProgress = () => {
    const delays = [500, 1500, 2500, 3500, 4500];
    delays.forEach((delay, index) => {
      setTimeout(() => {
        setLoadingSteps(prev => prev.map((step, i) => {
          if (i < index) return { ...step, status: 'completed' };
          if (i === index) return { ...step, status: 'active' };
          return step;
        }));
      }, delay);
    });
  };

  const resetProgress = () => {
    setLoadingSteps(prev => prev.map(step => ({ ...step, status: 'pending' })));
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setView('loading');
    resetProgress();
    simulateProgress();
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('vehicle_make', selectedVehicle.make);
    formData.append('vehicle_model', selectedVehicle.model);
    formData.append('vehicle_year', selectedVehicle.year);
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        let errMessage = 'Failed to analyze image';
        try {
          const errorData = await response.json();
          if (errorData.error) errMessage = errorData.error;
        } catch (e) {}
        throw new Error(errMessage);
      }
      
      const data = await response.json();
      setResult(data);
      // Wait a moment for final step animation before transitioning
      setTimeout(() => setView('results'), 500);
    } catch (err) {
      setError(err.message);
      setView('inspect'); // Go back on error
    }
  };

  const resetToInspect = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setView('inspect');
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header onNavigate={setView} />
      
      <main className="flex-1 w-full pb-20">
        {view === 'home' && (
          <div className="fade-in">
            <Hero onStart={() => setView('inspect')} />
            <HowItWorks />
            <WhatWeDetect />
            <HelpFAQ />
          </div>
        )}

        {view === 'inspect' && (
          <div className="max-w-6xl mx-auto px-6 py-12 fade-in">
            <div className="text-center mb-10">
              <h1 className="font-display text-3xl font-bold text-neutral-900 mb-3">Inspect Your Vehicle</h1>
              <p className="text-neutral-600 max-w-xl mx-auto">
                Upload a clear photo of the damage. We'll identify the affected parts and estimate the repair cost.
              </p>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-1 flex flex-col gap-6">
                <VehicleDetailsForm selectedVehicle={selectedVehicle} onVehicleChange={setSelectedVehicle} />
                <PhotoRequirements />
              </div>
              <div className="lg:col-span-2">
                <UploadArea 
                  file={file} 
                  preview={preview} 
                  onFileSelect={handleFileSelection} 
                  onAnalyze={handleAnalyze} 
                />
                {error && (
                  <div className="mt-4 p-4 bg-rose-50 border border-rose-200 rounded-xl text-rose-700 text-sm">
                    <strong>Upload failed:</strong> {error}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {view === 'loading' && (
          <div className="max-w-6xl mx-auto px-6 py-24 flex items-center justify-center fade-in">
            <LoadingProgress steps={loadingSteps} />
          </div>
        )}

        {view === 'results' && (
          <div className="fade-in">
            <ResultsDashboard result={result} onReset={resetToInspect} />
          </div>
        )}
      </main>

      <Footer onNavigate={setView} />
    </div>
  );
}
