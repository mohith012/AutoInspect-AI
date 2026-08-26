import React, { useRef, useState, useEffect } from 'react';
import { UploadCloud, Image as ImageIcon, Camera, AlertTriangle, X, Aperture } from 'lucide-react';

export default function UploadArea({ file, preview, onFileSelect, onAnalyze }) {
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  
  const [dragActive, setDragActive] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraError, setCameraError] = useState('');
  const [stream, setStream] = useState(null);

  // Clean up media stream when component unmounts or camera closes
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
    setIsCameraOpen(false);
  };

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

  const startCamera = async (e) => {
    if (e) e.stopPropagation();
    setCameraError('');
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ 
        video: { facingMode: 'environment' } 
      });
      setStream(mediaStream);
      setIsCameraOpen(true);
    } catch (err) {
      setCameraError('Camera access denied or not available. Please check permissions.');
    }
  };

  // Attach stream to video once the state updates and videoRef is available
  useEffect(() => {
    if (isCameraOpen && videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [isCameraOpen, stream]);

  const capturePhoto = (e) => {
    e.stopPropagation();
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob((blob) => {
        if (blob) {
          const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
          onFileSelect(file);
          stopCamera();
        }
      }, 'image/jpeg', 0.9);
    }
  };

  if (isCameraOpen) {
    return (
      <div className="w-full relative glass-panel overflow-hidden bg-black flex flex-col items-center justify-center min-h-[400px]">
        {cameraError ? (
          <div className="p-6 text-center">
            <AlertTriangle className="w-12 h-12 text-primary mx-auto mb-4" />
            <p className="text-white mb-4">{cameraError}</p>
            <button className="btn-secondary" onClick={() => setIsCameraOpen(false)}>Close Camera</button>
          </div>
        ) : (
          <>
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              className="w-full h-[400px] object-cover"
            />
            <canvas ref={canvasRef} className="hidden" />
            
            {/* Camera Overlay UI */}
            <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-30">
              <svg viewBox="0 0 400 200" className="w-3/4 max-w-md text-white" fill="none" stroke="currentColor" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round">
                <path d="M 60 140 L 40 140 C 25 140 20 130 20 120 L 25 90 C 27 75 40 70 50 70 L 100 60 L 140 20 C 150 10 170 5 190 5 L 260 5 C 280 5 300 15 310 30 L 340 70 L 360 70 C 375 70 380 80 380 95 L 380 140 C 380 150 370 150 360 150 L 335 150 M 60 140 A 30 30 0 0 1 120 140 M 335 140 A 30 30 0 0 0 275 140 M 120 140 L 275 140" />
              </svg>
            </div>
            
            <div className="absolute bottom-6 left-0 right-0 flex justify-center items-center gap-6 z-10">
              <button 
                className="bg-white/20 hover:bg-white/30 backdrop-blur text-white p-3 rounded-full transition-colors"
                onClick={(e) => { e.stopPropagation(); stopCamera(); }}
              >
                <X className="w-6 h-6" />
              </button>
              
              <button 
                className="bg-primary hover:bg-primary-hover text-white p-4 rounded-full shadow-[0_0_20px_rgba(246,33,33,0.5)] transition-transform hover:scale-105"
                onClick={capturePhoto}
              >
                <Aperture className="w-8 h-8" />
              </button>
            </div>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="w-full">
      {!preview ? (
        <div 
          tabIndex="0"
          className={`relative border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center min-h-[400px] transition-colors focus:outline-none focus:ring-4 focus:ring-primary/20 ${
            dragActive ? 'border-primary bg-primary/5' : 'border-gray-300 bg-gray-50/50 hover:bg-gray-100 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-[0.03]">
            <svg viewBox="0 0 400 200" className="w-3/4 max-w-md" fill="none" stroke="currentColor" strokeWidth="8" strokeLinecap="round" strokeLinejoin="round">
              <path d="M 60 140 L 40 140 C 25 140 20 130 20 120 L 25 90 C 27 75 40 70 50 70 L 100 60 L 140 20 C 150 10 170 5 190 5 L 260 5 C 280 5 300 15 310 30 L 340 70 L 360 70 C 375 70 380 80 380 95 L 380 140 C 380 150 370 150 360 150 L 335 150 M 60 140 A 30 30 0 0 1 120 140 M 335 140 A 30 30 0 0 0 275 140 M 120 140 L 275 140" />
            </svg>
          </div>

          <UploadCloud className="w-16 h-16 text-gray-400 mb-4" />
          <h3 className="text-xl font-display font-semibold text-dark mb-2">Upload vehicle photo</h3>
          <p className="text-gray-500 text-sm text-center max-w-sm mb-6">
            Drag and drop, paste (Ctrl+V), or click to browse. Ensure the vehicle is aligned well.
          </p>

          <div className="flex gap-4 relative z-10">
            <button className="btn-secondary" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
              <ImageIcon className="w-4 h-4" /> Upload Photo
            </button>
            <button className="btn-primary" onClick={startCamera}>
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
        </div>
      ) : (
        <div className="glass-panel p-6">
          <div className="bg-gray-100 rounded-xl p-2 mb-6 relative overflow-hidden">
            <img src={preview} alt="Vehicle Preview" className="w-full h-auto max-h-[500px] object-contain rounded-lg" />
            
            <div className="absolute top-4 left-4 right-4 bg-white/95 backdrop-blur shadow-lg rounded-lg p-4 flex gap-3 border-l-4 border-amber-500">
              <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
              <div>
                <p className="text-sm font-semibold text-dark">Check photo quality</p>
                <p className="text-xs text-gray-600 mt-1">If the photo has strong glare or the vehicle is heavily cropped, the AI might miss some damages.</p>
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
