import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { Hotel, Utensils, HeartPulse, Train, MapPin } from 'lucide-react';

// Fix for default Leaflet icon assets loading issue in Vite
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

// Helper component to programmatically reposition the map view when coords change
const ChangeMapView = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, map.getZoom());
  }, [center, map]);
  return null;
};

export const MapComponent = ({ destName, lat, lng, nearbyServices = [] }) => {
  const [activeFilters, setActiveFilters] = useState({
    Hotel: true,
    Restaurant: true,
    Hospital: true,
    Transport: true,
  });

  const center = [lat, lng];

  // Icon Generators using Tailwind CSS divs (eliminates path bugs, looks flat and modern)
  const createDivIcon = (colorClass, type) => {
    let dotHtml = '<span class="block w-2.5 h-2.5 rounded-full bg-white animate-pulse"></span>';
    
    return L.divIcon({
      className: 'custom-leaflet-marker',
      html: `<div class="w-8 h-8 rounded-full ${colorClass} border-2 border-white flex items-center justify-center shadow-md text-white">${dotHtml}</div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
      popupAnchor: [0, -32]
    });
  };

  const destinationIcon = L.divIcon({
    className: 'custom-destination-marker',
    html: `<div class="w-10 h-10 rounded-full bg-emerald-600 border-2 border-white flex items-center justify-center shadow-lg text-white animate-bounce">
             <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
           </div>`,
    iconSize: [40, 40],
    iconAnchor: [20, 40],
    popupAnchor: [0, -40]
  });

  // Services list mapping
  const serviceMarkers = nearbyServices.map((service) => {
    let colorClass = 'bg-blue-500';
    let icon = <Hotel className="w-4 h-4" />;
    
    if (service.type === 'Restaurant') {
      colorClass = 'bg-amber-500';
      icon = <Utensils className="w-4 h-4" />;
    } else if (service.type === 'Hospital') {
      colorClass = 'bg-rose-500';
      icon = <HeartPulse className="w-4 h-4" />;
    } else if (service.type === 'Transport') {
      colorClass = 'bg-purple-500';
      icon = <Train className="w-4 h-4" />;
    }

    return {
      ...service,
      colorClass,
      icon,
      leafletIcon: createDivIcon(colorClass, service.type)
    };
  });

  // Filter markers based on checked state
  const visibleServices = serviceMarkers.filter(m => activeFilters[m.type]);

  const toggleFilter = (type) => {
    setActiveFilters(prev => ({ ...prev, [type]: !prev[type] }));
  };

  return (
    <div className="relative w-full h-[450px] rounded-2xl overflow-hidden shadow-inner border border-slate-200 dark:border-slate-800">
      {/* Map Filter Controls Overlay */}
      <div className="absolute top-4 right-4 z-[400] flex flex-wrap gap-2 max-w-[calc(100%-2rem)]">
        <button
          onClick={() => toggleFilter('Hotel')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-md border transition-all ${
            activeFilters.Hotel 
              ? 'bg-blue-600 border-blue-600 text-white' 
              : 'bg-white border-slate-200 text-slate-700 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200'
          }`}
        >
          <Hotel className="w-3.5 h-3.5" />
          <span>Hotels</span>
        </button>
        <button
          onClick={() => toggleFilter('Restaurant')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-md border transition-all ${
            activeFilters.Restaurant 
              ? 'bg-amber-500 border-amber-500 text-white' 
              : 'bg-white border-slate-200 text-slate-700 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200'
          }`}
        >
          <Utensils className="w-3.5 h-3.5" />
          <span>Food</span>
        </button>
        <button
          onClick={() => toggleFilter('Hospital')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-md border transition-all ${
            activeFilters.Hospital 
              ? 'bg-rose-500 border-rose-500 text-white' 
              : 'bg-white border-slate-200 text-slate-700 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200'
          }`}
        >
          <HeartPulse className="w-3.5 h-3.5" />
          <span>Hospitals</span>
        </button>
        <button
          onClick={() => toggleFilter('Transport')}
          className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold shadow-md border transition-all ${
            activeFilters.Transport 
              ? 'bg-purple-500 border-purple-500 text-white' 
              : 'bg-white border-slate-200 text-slate-700 dark:bg-slate-800 dark:border-slate-700 dark:text-slate-200'
          }`}
        >
          <Train className="w-3.5 h-3.5" />
          <span>Transport</span>
        </button>
      </div>

      {/* Leaflet Map */}
      <MapContainer 
        center={center} 
        zoom={14} 
        scrollWheelZoom={false}
        className="w-full h-full"
      >
        <ChangeMapView center={center} />
        
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />

        {/* Primary Destination Pin */}
        <Marker position={center} icon={destinationIcon}>
          <Popup className="custom-leaflet-popup">
            <div className="p-1">
              <h3 className="font-extrabold text-slate-900 text-base">{destName}</h3>
              <p className="text-xs text-emerald-600 font-bold flex items-center gap-1 mt-1">
                <MapPin className="w-3 h-3" /> Tourist Spot (Center)
              </p>
            </div>
          </Popup>
        </Marker>

        {/* Render visible services */}
        {visibleServices.map((service, idx) => (
          <Marker 
            key={idx} 
            position={[service.latitude, service.longitude]} 
            icon={service.leafletIcon}
          >
            <Popup>
              <div className="p-1">
                <div className="flex items-center gap-1.5">
                  <span className={`p-1 rounded-lg text-white ${service.colorClass}`}>
                    {service.icon}
                  </span>
                  <h4 className="font-bold text-slate-800 text-sm">{service.name}</h4>
                </div>
                <p className="text-xs text-slate-500 mt-1.5">Type: <b>{service.type}</b></p>
                {service.contact && (
                  <p className="text-xs text-slate-600 mt-1">
                    📞 Contact: <a href={`tel:${service.contact}`} className="text-emerald-600 underline font-semibold">{service.contact}</a>
                  </p>
                )}
              </div>
            </Popup>
          </Marker>
        ))}

        {/* Drawing route trails to nearby services */}
        {visibleServices.map((service, idx) => (
          <Polyline 
            key={`route-${idx}`}
            positions={[center, [service.latitude, service.longitude]]}
            pathOptions={{ 
              color: service.type === 'Hospital' ? '#ef4444' : service.type === 'Hotel' ? '#3b82f6' : '#94a3b8',
              dashArray: '5, 10', 
              weight: 2, 
              opacity: 0.6 
            }}
          />
        ))}
      </MapContainer>
    </div>
  );
};

export default MapComponent;
