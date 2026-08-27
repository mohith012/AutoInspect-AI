import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { MapPin, Navigation, Phone, Search, AlertCircle, Loader2 } from 'lucide-react';

// Fix for default marker icons in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Custom icon for user location
const userIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

export default function NearbyShops({ assessmentResult }) {
  const [locationState, setLocationState] = useState('idle'); // idle, requesting, granted, denied, error
  const [coordinates, setCoordinates] = useState(null);
  const [shops, setShops] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [radius, setRadius] = useState(5000);

  const requestLocation = () => {
    setLocationState('requesting');
    if (!navigator.geolocation) {
      setLocationState('error');
      setError('Geolocation is not supported by your browser.');
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocationState('granted');
        setCoordinates({
          lat: position.coords.latitude,
          lon: position.coords.longitude
        });
      },
      (error) => {
        setLocationState('denied');
        if (error.code === error.PERMISSION_DENIED) {
          setError('Location access was denied. Please allow location access to find nearby shops.');
        } else {
          setError('Unable to retrieve your location.');
        }
      }
    );
  };

  useEffect(() => {
    if (locationState === 'granted' && coordinates) {
      fetchShops();
    }
  }, [locationState, coordinates, radius]);

  const fetchShops = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/nearby-shops?lat=${coordinates.lat}&lon=${coordinates.lon}&radius=${radius}`);
      if (!response.ok) throw new Error('Failed to fetch shops');
      const data = await response.json();
      setShops(data.shops || []);
    } catch (err) {
      setError(err.message || 'An error occurred while fetching shops.');
    } finally {
      setLoading(false);
    }
  };

  if (locationState === 'idle') {
    return (
      <div className="glass-panel p-8 text-center mt-8">
        <div className="w-16 h-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <MapPin className="w-8 h-8" />
        </div>
        <h3 className="font-display text-xl font-bold text-neutral-900 mb-2">Find Nearby Repair Shops</h3>
        <p className="text-neutral-600 mb-6 max-w-md mx-auto">
          We can help you find local mechanics and auto body shops. Allow location access to see places near you.
        </p>
        <button onClick={requestLocation} className="btn-primary">
          <Search className="w-4 h-4 mr-2" /> Allow Location & Search
        </button>
      </div>
    );
  }

  if (locationState === 'requesting') {
    return (
      <div className="glass-panel p-12 text-center mt-8 flex flex-col items-center">
        <Loader2 className="w-8 h-8 text-blue-600 animate-spin mb-4" />
        <h3 className="font-display text-lg font-bold text-neutral-900">Requesting Location...</h3>
      </div>
    );
  }

  if (locationState === 'denied' || locationState === 'error') {
    return (
      <div className="glass-panel p-8 text-center mt-8">
        <div className="w-16 h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h3 className="font-display text-xl font-bold text-neutral-900 mb-2">Location Access Failed</h3>
        <p className="text-red-600 mb-6">{error}</p>
        <button onClick={requestLocation} className="btn-secondary">
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="mt-8 flex flex-col gap-6">
      <div className="flex justify-between items-end">
        <div>
          <h3 className="font-display text-xl font-bold text-neutral-900">Nearby Repair Shops</h3>
          <p className="text-sm text-neutral-500">Based on your current location</p>
        </div>
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium text-neutral-700">Search Radius:</label>
          <select 
            value={radius} 
            onChange={(e) => setRadius(Number(e.target.value))}
            className="input-field py-1 px-3 min-h-0 h-9"
          >
            <option value={2000}>2 km</option>
            <option value={5000}>5 km</option>
            <option value={10000}>10 km</option>
            <option value={20000}>20 km</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map View */}
        <div className="lg:col-span-1 rounded-2xl overflow-hidden shadow-sm border border-neutral-200 h-[400px] z-0 relative">
          {coordinates && (
            <MapContainer center={[coordinates.lat, coordinates.lon]} zoom={13} style={{ height: '100%', width: '100%' }}>
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              <Marker position={[coordinates.lat, coordinates.lon]} icon={userIcon}>
                <Popup>You are here</Popup>
              </Marker>
              {shops.map((shop) => (
                <Marker key={shop.id} position={[shop.lat, shop.lon]}>
                  <Popup>
                    <strong>{shop.name}</strong><br />
                    {shop.distance} km away
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          )}
        </div>

        {/* Results List */}
        <div className="lg:col-span-2 flex flex-col gap-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
            </div>
          ) : shops.length === 0 ? (
            <div className="glass-panel p-8 text-center h-full flex flex-col items-center justify-center">
              <p className="text-neutral-500">No shops found within {radius / 1000}km.</p>
            </div>
          ) : (
            shops.map((shop) => (
              <div key={shop.id} className="glass-panel p-5 flex flex-col sm:flex-row justify-between gap-4">
                <div>
                  <h4 className="font-bold text-neutral-900">{shop.name}</h4>
                  <p className="text-sm text-neutral-500 mb-2">{shop.category} • {shop.distance} km away</p>
                  <p className="text-sm text-neutral-600">{shop.address}</p>
                </div>
                <div className="flex flex-row sm:flex-col gap-2 shrink-0">
                  <a 
                    href={`https://www.google.com/maps/dir/?api=1&origin=${coordinates.lat},${coordinates.lon}&destination=${shop.lat},${shop.lon}`} 
                    target="_blank" 
                    rel="noreferrer"
                    className="btn-primary text-xs py-2 px-3 flex-1 flex justify-center"
                  >
                    <Navigation className="w-3 h-3 mr-1" /> Directions
                  </a>
                  {shop.phone && (
                    <a 
                      href={`tel:${shop.phone}`} 
                      className="btn-secondary text-xs py-2 px-3 flex-1 flex justify-center"
                    >
                      <Phone className="w-3 h-3 mr-1" /> Call Shop
                    </a>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
