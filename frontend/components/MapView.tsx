"use client";

import { MapContainer, TileLayer, Marker, Popup, Circle } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { FaHospital, FaPhone, FaClock, FaGlobe } from "react-icons/fa";

// Fix for default marker icons in Next.js
// @ts-expect-error - Leaflet icon fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl:
    "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

// Custom hospital icon
const hospitalIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// User location icon
const userIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

interface Hospital {
  name: string;
  rating?: number;
  user_ratings_total?: number;
  vicinity: string;
  place_id: string;
  lat: number;
  lng: number;
  phone?: string;
  opening_hours?: string;
  website?: string;
  distance_km?: number;
}

interface MapViewProps {
  hospitals: Hospital[];
  userLocation: { lat: number; lng: number } | null;
  radius: number;
}

export default function MapView({
  hospitals,
  userLocation,
  radius,
}: MapViewProps) {
  const defaultCenter: [number, number] = userLocation
    ? [userLocation.lat, userLocation.lng]
    : [37.7749, -122.4194]; // San Francisco default

  return (
    <div className="w-full h-[600px] rounded-xl overflow-hidden border border-white/10 shadow-2xl">
      <MapContainer
        center={defaultCenter}
        zoom={13}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* User location marker and radius */}
        {userLocation && (
          <>
            <Marker
              position={[userLocation.lat, userLocation.lng]}
              icon={userIcon}
            >
              <Popup>
                <div className="text-sm">
                  <strong>Your Location</strong>
                  <br />
                  {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
                </div>
              </Popup>
            </Marker>
            <Circle
              center={[userLocation.lat, userLocation.lng]}
              radius={radius}
              pathOptions={{
                color: "#0ea5e9",
                fillColor: "#0ea5e9",
                fillOpacity: 0.1,
              }}
            />
          </>
        )}

        {/* Hospital markers */}
        {hospitals.map((hospital, index) => (
          <Marker
            key={index}
            position={[hospital.lat, hospital.lng]}
            icon={hospitalIcon}
          >
            <Popup maxWidth={300}>
              <div className="text-sm space-y-2 p-2">
                <div className="flex items-start space-x-2">
                  <FaHospital className="text-red-500 text-lg flex-shrink-0 mt-1" />
                  <div>
                    <strong className="text-base block mb-1">
                      {hospital.name}
                    </strong>
                    <p className="text-gray-600 text-xs">{hospital.vicinity}</p>
                  </div>
                </div>

                {hospital.distance_km && (
                  <div className="text-xs text-gray-500">
                    📍 {hospital.distance_km} km away
                  </div>
                )}

                {hospital.phone && (
                  <div className="flex items-center space-x-2 text-xs">
                    <FaPhone className="text-green-600" />
                    <a
                      href={`tel:${hospital.phone}`}
                      className="text-blue-600 hover:underline"
                    >
                      {hospital.phone}
                    </a>
                  </div>
                )}

                {hospital.opening_hours && (
                  <div className="flex items-center space-x-2 text-xs">
                    <FaClock className="text-orange-600" />
                    <span className="text-gray-600">
                      {hospital.opening_hours}
                    </span>
                  </div>
                )}

                {hospital.website && (
                  <div className="flex items-center space-x-2 text-xs">
                    <FaGlobe className="text-blue-600" />
                    <a
                      href={hospital.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      Visit Website
                    </a>
                  </div>
                )}

                <a
                  href={`https://www.google.com/maps/search/?api=1&query=${hospital.lat},${hospital.lng}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full mt-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-center rounded text-xs font-semibold transition-colors"
                >
                  Get Directions
                </a>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
