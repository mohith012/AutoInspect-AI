import { useState, useEffect } from 'react'
import { UploadCloud, CheckCircle, AlertTriangle, AlertCircle, Loader2, Car } from 'lucide-react'

const VEHICLES = [
  { id: 'generic', label: "Generic Hatchback (Fallback)", make: "Generic", model: "Hatchback", year: 2022 },
  { id: 'swift', label: "Maruti Suzuki Swift", make: "Maruti Suzuki", model: "Swift", year: 2022 },
  { id: 'wagonr', label: "Maruti Suzuki WagonR", make: "Maruti Suzuki", model: "WagonR", year: 2022 },
  { id: 'baleno', label: "Maruti Suzuki Baleno", make: "Maruti Suzuki", model: "Baleno", year: 2022 },
  { id: 'nexon', label: "Tata Nexon (Compact SUV)", make: "Tata", model: "Nexon", year: 2022 },
  { id: 'creta', label: "Hyundai Creta (SUV)", make: "Hyundai", model: "Creta", year: 2022 },
  { id: 'i20', label: "Hyundai i20", make: "Hyundai", model: "i20", year: 2022 },
];

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [selectedVehicle, setSelectedVehicle] = useState(VEHICLES[0])

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    handleFileSelection(selected)
  }

  const handleFileSelection = (selected) => {
    if (selected && selected.type.startsWith('image/')) {
      setFile(selected)
      setPreview(URL.createObjectURL(selected))
      setResult(null)
      setError(null)
    }
  }

  useEffect(() => {
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
  }, []);

  const handleUpload = async () => {
    if (!file) return
    
    setLoading(true)
    setError(null)
    
    const formData = new FormData()
    formData.append('file', file)
    formData.append('vehicle_make', selectedVehicle.make)
    formData.append('vehicle_model', selectedVehicle.model)
    formData.append('vehicle_year', selectedVehicle.year)
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData
      })
      
      if (!response.ok) {
        throw new Error('Failed to analyze image')
      }
      
      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getRecommendationColor = (rec) => {
    if (!rec) return 'bg-slate-700 text-slate-300 border-slate-600'
    const r = rec.toLowerCase()
    if (r === 'repair') return 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
    if (r === 'replace') return 'bg-red-500/20 text-red-400 border-red-500/30'
    return 'bg-amber-500/20 text-amber-400 border-amber-500/30'
  }

  const getRecommendationIcon = (rec) => {
    if (!rec) return null
    const r = rec.toLowerCase()
    if (r === 'repair') return <CheckCircle className="w-6 h-6" />
    if (r === 'replace') return <AlertTriangle className="w-6 h-6" />
    return <AlertCircle className="w-6 h-6" />
  }

  return (
    <div className="max-w-6xl mx-auto p-6 min-h-screen flex flex-col pt-12">
      
      <header className="mb-12 text-center">
        <h1 className="text-4xl font-extrabold bg-gradient-to-r from-indigo-400 via-cyan-400 to-emerald-400 bg-clip-text text-transparent inline-block mb-4">
          AutoInspect AI
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto">
          Upload an image of vehicle damage to instantly receive a professional AI-driven repair vs replace assessment.
        </p>
      </header>

      <main className="flex-1 w-full grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        
        {/* Upload Column */}
        <div className="flex flex-col gap-6">
          <div className="glass-panel p-6 flex flex-col gap-3">
            <label className="text-sm font-bold text-slate-300 uppercase tracking-wider flex items-center gap-2">
              <Car className="w-4 h-4 text-indigo-400" />
              Select Vehicle Type
            </label>
            <select 
              className="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-3 outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition"
              value={selectedVehicle.id}
              onChange={(e) => setSelectedVehicle(VEHICLES.find(v => v.id === e.target.value))}
            >
              {VEHICLES.map(v => (
                <option key={v.id} value={v.id}>{v.label}</option>
              ))}
            </select>
            <p className="text-xs text-slate-500">
              Pricing and labor rates are customized based on the vehicle model and tier (Hatchback/SUV).
            </p>
          </div>

          <div className="glass-panel p-8 w-full flex flex-col items-center justify-center min-h-[400px]">
          
          {!preview ? (
            <label className="w-full flex-1 flex flex-col items-center justify-center border-2 border-dashed border-slate-600 rounded-xl hover:border-indigo-500 hover:bg-slate-800/50 transition-all cursor-pointer group">
              <UploadCloud className="w-16 h-16 text-slate-500 group-hover:text-indigo-400 mb-4 transition-colors" />
              <span className="text-lg font-medium text-slate-300">Click, drag, or paste image to upload</span>
              <span className="text-sm text-slate-500 mt-2">JPEG, PNG up to 10MB</span>
              <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
            </label>
          ) : (
            <div className="w-full flex flex-col items-center">
              <div className="relative w-full rounded-xl overflow-hidden shadow-2xl mb-6 bg-black/50">
                <img 
                  src={result ? `http://localhost:8000${result.image_url}` : preview} 
                  alt="Vehicle Preview" 
                  className="w-full h-auto max-h-[500px] object-contain"
                />
              </div>
              
              <div className="flex gap-4 w-full">
                <label className="flex-1 py-3 px-4 text-center rounded-lg border border-slate-600 hover:bg-slate-700 transition cursor-pointer font-medium">
                  Choose Another
                  <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                </label>
                
                {!result && (
                  <button 
                    onClick={handleUpload}
                    disabled={loading}
                    className="flex-1 py-3 px-4 bg-indigo-600 hover:bg-indigo-500 disabled:bg-indigo-800 disabled:cursor-not-allowed text-white font-semibold rounded-lg shadow-lg shadow-indigo-900/50 transition flex items-center justify-center gap-2"
                  >
                    {loading ? (
                      <><Loader2 className="w-5 h-5 animate-spin" /> Analyzing...</>
                    ) : (
                      'Run AI Pipeline'
                    )}
                  </button>
                )}
              </div>
            </div>
          )}

          {error && (
            <div className="mt-6 w-full p-4 bg-red-900/30 border border-red-500/50 rounded-lg flex items-center gap-3 text-red-200">
              <AlertTriangle className="w-5 h-5 text-red-400 shrink-0" />
              <p>{error}</p>
            </div>
          )}
          </div>
        </div>

        {/* Results Column */}
        <div className="flex flex-col gap-6">
          {loading && (
            <div className="glass-panel p-12 flex flex-col items-center justify-center text-slate-400 h-full min-h-[400px]">
              <Loader2 className="w-12 h-12 animate-spin text-indigo-500 mb-6" />
              <p className="text-xl font-medium animate-pulse">Running AI Pipeline...</p>
              <div className="mt-4 space-y-2 text-sm text-slate-500 text-center">
                <p>1. Detecting Damages (YOLOv8)</p>
                <p>2. Identifying Vehicle Parts (YOLOv8)</p>
                <p>3. Geometric Spatial Mapping</p>
                <p>4. Padding & Extracting Crops</p>
                <p>5. Estimating Severity (MobileNetV2)</p>
                <p>6. Evaluating Decision Engine Rules</p>
              </div>
            </div>
          )}
          
          {!loading && !result && (
            <div className="glass-panel p-12 flex flex-col items-center justify-center text-slate-500 h-full min-h-[400px] border-dashed">
              <p className="text-lg">Upload an image to see the assessment results here.</p>
            </div>
          )}

          {!loading && result && (
            <>
              {/* Overall Recommendation */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className={`glass-panel p-6 border-2 flex items-center gap-6 ${getRecommendationColor(result.overall_recommendation)}`}>
                  <div className="shrink-0">
                    {getRecommendationIcon(result.overall_recommendation)}
                  </div>
                  <div>
                    <h2 className="text-sm font-bold uppercase tracking-wider opacity-80 mb-1">Overall Verdict</h2>
                    <p className="text-3xl font-black uppercase tracking-tight">
                      {result.overall_recommendation}
                    </p>
                  </div>
                </div>

                {result.total_cost_estimate && result.total_cost_estimate.max > 0 && (
                  <div className="glass-panel p-6 border-2 border-indigo-500/30 bg-indigo-900/20 flex flex-col justify-center">
                    <h2 className="text-sm font-bold uppercase tracking-wider text-indigo-300 mb-1">Estimated Total Cost</h2>
                    <p className="text-2xl font-black text-indigo-100">
                      ₹{result.total_cost_estimate.min.toLocaleString()} – ₹{result.total_cost_estimate.max.toLocaleString()}
                    </p>
                    <p className="text-xs text-indigo-400 mt-1">Data Quality: {result.price_data_quality?.toUpperCase()}</p>
                  </div>
                )}
              </div>

              {/* Performance Metrics */}
              <div className="glass-panel p-5 flex justify-between text-xs text-slate-400">
                <span>Model 1: {result.performance['Model 1 (ms)']}ms</span>
                <span>Model 2: {result.performance['Model 2 (ms)']}ms</span>
                <span>Severity: {result.performance['Model 3 (ms)']}ms</span>
                <span className="text-indigo-400 font-semibold">Total: {result.performance['Total (ms)']}ms</span>
              </div>

              {/* Damage List */}
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-slate-200 ml-1">Detected Damages ({result.damages?.length || 0})</h3>
                
                {result.damages?.length === 0 && (
                  <div className="glass-card p-6 text-center text-slate-400">
                    No visible damage detected on supported parts.
                  </div>
                )}
                
                {result.damages?.map((damage, i) => (
                  <div key={i} className="glass-card p-5 hover:border-slate-500/50">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="flex items-center gap-3 mb-1">
                          <span className="text-lg font-bold text-indigo-300 capitalize">{damage.damaged_part}</span>
                          <span className="text-slate-500">→</span>
                          <span className="text-lg font-bold text-cyan-300 capitalize">{damage.damage_type}</span>
                        </div>
                        <div className="flex gap-2 text-xs">
                          <span className="bg-slate-700/50 px-2 py-1 rounded">Part Conf: {Math.round((damage.part_confidence || 0)*100)}%</span>
                          <span className="bg-slate-700/50 px-2 py-1 rounded">Damage Conf: {Math.round((damage.damage_confidence || 0)*100)}%</span>
                        </div>
                      </div>
                      
                      <div className="flex flex-col items-end">
                        <span className="text-sm font-semibold uppercase tracking-wider text-slate-300 mb-1">Severity</span>
                        <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase border ${
                          damage.severity === 'severe' ? 'bg-red-500/20 text-red-400 border-red-500/30' :
                          damage.severity === 'moderate' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' :
                          damage.severity === 'minor' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' :
                          'bg-slate-700 text-slate-300 border-slate-600'
                        }`}>
                          {damage.severity} ({(damage.severity_confidence || 0).toFixed(2)})
                        </span>
                      </div>
                    </div>
                    
                    <div className={`mt-4 p-4 rounded-lg border ${getRecommendationColor(damage.recommendation)} bg-opacity-10`}>
                      <div className="flex items-center gap-2 mb-2 font-bold uppercase text-sm">
                        {getRecommendationIcon(damage.recommendation)}
                        {damage.recommendation}
                      </div>
                      <p className="text-sm opacity-90 leading-relaxed mb-3">{damage.reason}</p>
                      
                      {damage.cost_estimate && (
                        <div className="bg-black/30 rounded-lg p-3 text-sm">
                          {damage.cost_estimate.total_cost && damage.cost_estimate.total_cost.max > 0 ? (
                            <div className="grid grid-cols-2 gap-2 text-slate-300">
                              {damage.cost_estimate.part_cost?.max > 0 && (
                                <>
                                  <span className="text-slate-400">Part Cost:</span>
                                  <span className="text-right">₹{damage.cost_estimate.part_cost.min.toLocaleString()} – ₹{damage.cost_estimate.part_cost.max.toLocaleString()}</span>
                                </>
                              )}
                              {damage.cost_estimate.repair_cost?.max > 0 && (
                                <>
                                  <span className="text-slate-400">Repair Cost:</span>
                                  <span className="text-right">₹{damage.cost_estimate.repair_cost.min.toLocaleString()} – ₹{damage.cost_estimate.repair_cost.max.toLocaleString()}</span>
                                </>
                              )}
                              <span className="text-slate-400">Labor:</span>
                              <span className="text-right">₹{damage.cost_estimate.labor_cost.min.toLocaleString()} – ₹{damage.cost_estimate.labor_cost.max.toLocaleString()}</span>
                              <div className="col-span-2 border-t border-slate-700/50 my-1"></div>
                              <span className="font-bold text-indigo-300">Total:</span>
                              <span className="font-bold text-indigo-300 text-right">₹{damage.cost_estimate.total_cost.min.toLocaleString()} – ₹{damage.cost_estimate.total_cost.max.toLocaleString()}</span>
                            </div>
                          ) : (
                            <p className="text-slate-400 italic text-xs">{damage.cost_estimate.message}</p>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </main>
      
      <footer className="mt-24 pb-8 text-center text-slate-500 text-sm">
        <p>AutoInspect AI • Computer Vision Damage Assessment</p>
      </footer>
    </div>
  )
}

export default App
