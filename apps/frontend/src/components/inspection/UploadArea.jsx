import React, { useRef, useState } from 'react';
import { UploadCloud, Image as ImageIcon, Camera, AlertTriangle } from 'lucide-react';

export default function UploadArea({ file, preview, onFileSelect, onAnalyze }) {
  const fileInputRef = useRef(null);
  const cameraInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleCameraClick = async (e) => {
    e.stopPropagation();
    try {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Request camera permission explicitly
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        // Stop the stream immediately as we just wanted to check/request permission
        stream.getTracks().forEach(track => track.stop());
      }
      // If permission granted or not supported (fallback), trigger the native camera input
      cameraInputRef.current?.click();
    } catch (err) {
      alert("Camera permission is required to use this feature. Please allow camera access in your browser settings.");
    }
  };

  return (
    <div className="w-full">
      {!preview ? (
        <div 
          tabIndex="0"
          className={`relative border-2 border-dashed rounded-2xl p-8 flex flex-col items-center justify-center min-h-[400px] transition-colors focus:outline-none focus:ring-4 focus:ring-red-500/20 ${
            dragActive ? 'border-red-500 bg-red-50/50' : 'border-neutral-300 bg-neutral-50/50 hover:bg-neutral-100 hover:border-neutral-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {/* Conceptual Car Guide Overlay */}
          <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-[0.03]">
            <svg viewBox="0 0 400 200" className="w-3/4 max-w-md" fill="none" stroke="currentColor" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M 60 140 L 40 140 C 25 140 20 130 20 120 L 25 90 C 27 75 40 70 50 70 L 100 60 L 140 20 C 150 10 170 5 190 5 L 260 5 C 280 5 300 15 310 30 L 340 70 L 360 70 C 375 70 380 80 380 95 L 380 140 C 380 150 370 150 360 150 L 335 150 M 60 140 A 30 30 0 0 1 120 140 M 335 140 A 30 30 0 0 0 275 140 M 120 140 L 275 140" />
            </svg>
          </div>

          <UploadCloud className="w-16 h-16 text-neutral-400 mb-4" />
          <h3 className="text-xl font-semibold text-neutral-900 mb-2">Upload vehicle photo</h3>
          <p className="text-neutral-500 text-sm text-center max-w-sm mb-6">
            Drag and drop, paste (Ctrl+V), or click to browse. Ensure the vehicle is aligned well.
          </p>

          <div className="flex gap-4 relative z-10">
            <button className="btn-secondary" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
              <ImageIcon className="w-4 h-4" /> Upload Photo
            </button>
            <button className="btn-primary" onClick={handleCameraClick}>
              <Camera className="w-4 h-4" /> Use Camera
            </button>
          </div>
          
          <input 
            type="file" 
            accept="image/jpeg, image/png, image/webp" 
            className="hidden" 
            ref={fileInputRef} 
            onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])} 
          />
          <input 
            type="file" 
            accept="image/*" 
            capture="environment"
            className="hidden" 
            ref={cameraInputRef} 
            onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])} 
          />
        </div>
      ) : (
        <div className="glass-panel p-6">
          <div className="bg-neutral-100 rounded-xl p-2 mb-6 relative overflow-hidden">
            <img src={preview} alt="Vehicle Preview" className="w-full h-auto max-h-[500px] object-contain rounded-lg" />
            
            {/* Friendly Validation Warning (Mocked logic for demo, usually tied to actual image metadata or quick ML pass) */}
            <div className="absolute top-4 left-4 right-4 bg-white/95 backdrop-blur shadow-lg rounded-lg p-4 flex gap-3 border-l-4 border-amber-500">
              <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-neutral-900">Check photo quality</p>
                <p className="text-xs text-neutral-600 mt-1">If the photo has strong glare or the vehicle is heavily cropped, the AI might miss some damages.</p>
              </div>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3">
            <button className="btn-secondary flex-1" onClick={() => onFileSelect(null)}>
              Try Another Photo
            </button>
            <button className="btn-primary flex-1" onClick={onAnalyze}>
              Analyze Vehicle
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
