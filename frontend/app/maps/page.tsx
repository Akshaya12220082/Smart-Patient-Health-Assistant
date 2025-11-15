"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import dynamic from "next/dynamic";
import {
  FaMapMarkerAlt,
  FaHospital,
  FaSearch,
  FaStar,
  FaDirections,
} from "react-icons/fa";

// Dynamically import map component to avoid SSR issues
const MapView = dynamic(() => import("../../components/MapView"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[500px] bg-gray-900 rounded-xl flex items-center justify-center">
      <div className="text-gray-400">Loading map...</div>
    </div>
  ),
});

interface Hospital {
  name: string;
  rating: number;
  user_ratings_total: number;
  vicinity: string;
  place_id: string;
  lat: number;
  lng: number;
}

export default function MapsPage() {
  const [selectedDisease, setSelectedDisease] = useState<string>("diabetes");
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(
    null
  );
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [radius, setRadius] = useState(5000);

  const diseases = [
    {
      id: "diabetes",
      name: "Diabetes / Endocrinology",
      icon: "🩺",
      description: "Endocrinology specialists and diabetes clinics",
    },
    {
      id: "heart",
      name: "Heart Disease / Cardiology",
      icon: "❤️",
      description: "Cardiologists and heart specialists",
    },
    {
      id: "kidney",
      name: "Kidney Disease / Nephrology",
      icon: "🫘",
      description: "Nephrologists and kidney disease specialists",
    },
  ];

  const [dataSource, setDataSource] = useState<string>("");

  const getDemoHospitals = (lat: number, lng: number) => {
    // Demo hospitals for when API is not configured
    return [
      {
        name: "City General Hospital",
        rating: 4.5,
        user_ratings_total: 1250,
        vicinity: "123 Main Street, Downtown",
        place_id: "demo_1",
        lat: lat + 0.01,
        lng: lng + 0.01,
      },
      {
        name: "Medical Center - Specialty Clinic",
        rating: 4.7,
        user_ratings_total: 890,
        vicinity: "456 Health Avenue, Medical District",
        place_id: "demo_2",
        lat: lat - 0.01,
        lng: lng + 0.015,
      },
      {
        name: "Community Healthcare Center",
        rating: 4.3,
        user_ratings_total: 650,
        vicinity: "789 Care Street, Uptown",
        place_id: "demo_3",
        lat: lat + 0.015,
        lng: lng - 0.01,
      },
      {
        name: "University Medical Center",
        rating: 4.8,
        user_ratings_total: 2100,
        vicinity: "321 University Boulevard",
        place_id: "demo_4",
        lat: lat - 0.015,
        lng: lng - 0.015,
      },
      {
        name: "Regional Health Clinic",
        rating: 4.2,
        user_ratings_total: 420,
        vicinity: "555 Wellness Way, East Side",
        place_id: "demo_5",
        lat: lat + 0.02,
        lng: lng,
      },
    ];
  };

  const findHospitals = () => {
    setLoading(true);
    setError(null);
    setHospitals([]);

    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser");
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setLocation({ lat: latitude, lng: longitude });

        try {
          const response = await fetch(
            `http://localhost:5001/hospitals/${selectedDisease}?lat=${latitude}&lng=${longitude}&radius=${radius}`
          );
          const data = await response.json();

          if (data.error) {
            // Check if it's an API configuration error
            if (
              response.status === 503 ||
              data.error.includes("not configured")
            ) {
              setError(
                "⚠️ Map services temporarily unavailable. Showing demo hospitals instead."
              );
              // Use demo data
              setHospitals(getDemoHospitals(latitude, longitude));
              setDataSource("Demo Mode");
            } else {
              setError(data.error + (data.details ? `: ${data.details}` : ""));
              setHospitals([]);
            }
          } else if (data.hospitals && Array.isArray(data.hospitals)) {
            console.log("✅ Received hospitals:", data.hospitals.length);
            setHospitals(data.hospitals);
            setDataSource(data.source || "Unknown");
            setError(null);
          } else {
            console.warn("No hospitals in response:", data);
            setError(
              "⚠️ No hospitals found in this area. Try increasing the search radius."
            );
            setHospitals([]);
          }
        } catch (err) {
          console.error("Failed to fetch hospitals:", err);
          setError(
            "⚠️ Cannot connect to backend. Showing demo hospitals instead."
          );
          // Use demo data as fallback
          setHospitals(getDemoHospitals(latitude, longitude));
          setDataSource("Demo Mode");
        } finally {
          setLoading(false);
        }
      },
      () => {
        setError(
          "Unable to retrieve your location. Please enable location services."
        );
        setLoading(false);
      }
    );
  };

  return (
    <div className="min-h-screen bg-black text-white pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex items-center justify-center mb-4">
            <FaMapMarkerAlt className="text-6xl text-primary-500" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-primary-400 to-cyan-400 bg-clip-text text-transparent">
            Find Nearby Specialists
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Locate hospitals, clinics, and specialized medical facilities near
            you based on your health needs.
          </p>
        </motion.div>

        {/* Disease Selection */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-8 mb-8"
        >
          <h2 className="text-2xl font-bold mb-6">Select Specialty</h2>
          <div className="grid md:grid-cols-3 gap-6">
            {diseases.map((disease) => (
              <button
                key={disease.id}
                onClick={() => setSelectedDisease(disease.id)}
                className={`p-6 rounded-xl border-2 transition-all text-left ${
                  selectedDisease === disease.id
                    ? "border-primary-500 bg-primary-500/10"
                    : "border-white/10 bg-white/5 hover:border-primary-500/50"
                }`}
              >
                <div className="text-4xl mb-3">{disease.icon}</div>
                <h3 className="text-lg font-bold mb-2">{disease.name}</h3>
                <p className="text-sm text-gray-400">{disease.description}</p>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Search Controls */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="glass rounded-2xl p-8 mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-end gap-6">
            <div className="flex-1">
              <label className="block text-sm font-medium mb-2">
                Search Radius
              </label>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min="1000"
                  max="50000"
                  step="1000"
                  value={radius}
                  onChange={(e) => setRadius(parseInt(e.target.value))}
                  className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
                />
                <input
                  type="number"
                  min="1"
                  max="50"
                  step="0.5"
                  value={(radius / 1000).toFixed(1)}
                  onChange={(e) => {
                    const km = parseFloat(e.target.value);
                    if (!isNaN(km) && km >= 1 && km <= 50) {
                      setRadius(Math.round(km * 1000));
                    }
                  }}
                  className="w-20 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-center focus:outline-none focus:border-primary-500"
                />
                <span className="text-sm font-semibold text-primary-400">
                  km
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Range: 1 - 50 km (Larger radius may take longer to search)
              </p>
            </div>

            <button
              onClick={findHospitals}
              disabled={loading}
              className="px-8 py-4 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-all hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center space-x-2"
            >
              <FaSearch />
              <span>{loading ? "Searching..." : "Find Hospitals"}</span>
            </button>
          </div>
        </motion.div>

        {/* Error/Warning Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className={`mb-8 p-6 rounded-xl ${
              error.startsWith("⚠️")
                ? "bg-yellow-900/20 border border-yellow-500 text-yellow-400"
                : "bg-red-900/20 border border-red-500 text-red-400"
            }`}
          >
            {error}
          </motion.div>
        )}

        {/* Location Info */}
        {location && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mb-8 p-6 bg-green-900/20 border border-green-500 rounded-xl text-green-400 flex items-center"
          >
            <FaMapMarkerAlt className="mr-3 text-2xl" />
            <div>
              <div className="font-semibold">Location Detected</div>
              <div className="text-sm">
                Coordinates: {location.lat.toFixed(6)},{" "}
                {location.lng.toFixed(6)}
              </div>
            </div>
          </motion.div>
        )}

        {/* Results */}
        {hospitals.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-3xl font-bold flex items-center">
                <FaHospital className="mr-3 text-primary-500" />
                Found {hospitals.length} Nearby Facilities
              </h2>
              {dataSource && (
                <span className="text-sm px-4 py-2 bg-primary-600/20 border border-primary-500/50 rounded-lg">
                  📍 {dataSource}
                </span>
              )}
            </div>

            {/* Interactive Map */}
            <div className="mb-8">
              <MapView
                hospitals={hospitals}
                userLocation={location}
                radius={radius}
              />
            </div>

            <div className="grid gap-6">
              {hospitals.map((hospital, index) => (
                <motion.div
                  key={hospital.place_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass rounded-2xl p-6 border border-white/10 hover:border-primary-500/50 transition-all"
                >
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold mb-2">
                        {hospital.name}
                      </h3>
                      <p className="text-gray-400 mb-4 flex items-center">
                        <FaMapMarkerAlt className="mr-2 text-primary-500" />
                        {hospital.vicinity}
                      </p>

                      <div className="flex items-center space-x-4">
                        {hospital.rating && (
                          <div className="flex items-center space-x-2">
                            <FaStar className="text-yellow-400" />
                            <span className="font-semibold">
                              {hospital.rating.toFixed(1)}
                            </span>
                            <span className="text-gray-500 text-sm">
                              ({hospital.user_ratings_total} reviews)
                            </span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex flex-col gap-3">
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=${hospital.lat},${hospital.lng}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-all hover:scale-105 flex items-center justify-center space-x-2"
                      >
                        <FaDirections />
                        <span>Get Directions</span>
                      </a>
                      <a
                        href={`https://www.google.com/maps/search/?api=1&query=Google&query_place_id=${hospital.place_id}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-6 py-3 bg-white/5 hover:bg-white/10 rounded-lg font-semibold transition-all text-center border border-white/10"
                      >
                        View Details
                      </a>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Empty State */}
        {!loading && !location && hospitals.length === 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20"
          >
            <FaHospital className="text-8xl text-gray-700 mx-auto mb-6" />
            <h3 className="text-2xl font-bold mb-3 text-gray-400">
              Ready to Find Hospitals
            </h3>
            <p className="text-gray-500 max-w-md mx-auto">
              Select a specialty and click &quot;Find Hospitals&quot; to
              discover nearby medical facilities.
            </p>
          </motion.div>
        )}
      </div>
    </div>
  );
}
