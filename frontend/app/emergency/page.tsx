"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  FaAmbulance,
  FaPhone,
  FaMapMarkerAlt,
  FaHospital,
  FaExclamationTriangle,
} from "react-icons/fa";

interface Hospital {
  name: string;
  rating: number;
  user_ratings_total: number;
  vicinity: string;
  place_id: string;
  lat: number;
  lng: number;
}

export default function EmergencyPage() {
  const [location, setLocation] = useState<{ lat: number; lng: number } | null>(
    null
  );
  const [hospitals, setHospitals] = useState<Hospital[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const emergencyNumbers = [
    { country: "USA", number: "911", icon: "🇺🇸" },
    { country: "India", number: "112", icon: "🇮🇳" },
    { country: "UK", number: "999", icon: "🇬🇧" },
    { country: "Australia", number: "000", icon: "🇦🇺" },
  ];

  const emergencySymptoms = [
    {
      title: "Chest Pain",
      description:
        "Severe chest pain or pressure lasting more than a few minutes",
      icon: "❤️",
    },
    {
      title: "Difficulty Breathing",
      description: "Sudden shortness of breath or trouble breathing",
      icon: "💨",
    },
    {
      title: "Severe Bleeding",
      description: "Uncontrolled bleeding or deep wounds",
      icon: "🩸",
    },
    {
      title: "Loss of Consciousness",
      description: "Fainting, seizures, or unresponsiveness",
      icon: "😵",
    },
    {
      title: "Severe Pain",
      description: "Sudden severe pain in any part of the body",
      icon: "⚡",
    },
    {
      title: "Stroke Symptoms",
      description: "Facial drooping, arm weakness, speech difficulty",
      icon: "🧠",
    },
  ];

  const getLocation = () => {
    setLoading(true);
    setError(null);

    if (!navigator.geolocation) {
      setError("Geolocation is not supported by your browser");
      setLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        setLocation({ lat: latitude, lng: longitude });

        // Fetch nearby hospitals
        try {
          const response = await fetch(
            `http://localhost:5001/hospitals/heart?lat=${latitude}&lng=${longitude}&radius=5000`
          );
          const data = await response.json();
          if (data.hospitals) {
            setHospitals(data.hospitals);
          }
        } catch (err) {
          console.error("Failed to fetch hospitals:", err);
          setError("Failed to fetch nearby hospitals");
        } finally {
          setLoading(false);
        }
      },
      (error) => {
        setError("Unable to retrieve your location");
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
            <FaAmbulance className="text-6xl text-red-500 animate-pulse" />
          </div>
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-red-400 to-orange-400 bg-clip-text text-transparent">
            Emergency Services
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Quick access to emergency contacts and nearby hospitals. In case of
            a medical emergency, call your local emergency number immediately.
          </p>
        </motion.div>

        {/* Emergency Alert */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="glass border-red-500/30 rounded-2xl p-8 mb-12 border-2"
        >
          <div className="flex items-start space-x-4">
            <FaExclamationTriangle className="text-red-500 text-4xl flex-shrink-0 mt-1" />
            <div>
              <h2 className="text-2xl font-bold text-red-500 mb-2">
                If This Is an Emergency
              </h2>
              <p className="text-gray-300 mb-4">
                Call your local emergency number immediately. Do not wait. Do
                not rely on online resources alone.
              </p>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {emergencyNumbers.map((item) => (
                  <a
                    key={item.country}
                    href={`tel:${item.number}`}
                    className="glass p-4 rounded-xl hover:border-red-500/50 border border-white/10 transition-all hover:scale-105"
                  >
                    <div className="text-3xl mb-2">{item.icon}</div>
                    <div className="text-sm text-gray-400">{item.country}</div>
                    <div className="text-2xl font-bold text-red-500">
                      {item.number}
                    </div>
                  </a>
                ))}
              </div>
            </div>
          </div>
        </motion.div>

        {/* Emergency Symptoms */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold mb-6 text-center">
            When to Call Emergency Services
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {emergencySymptoms.map((symptom, index) => (
              <motion.div
                key={symptom.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="glass p-6 rounded-xl hover:border-primary-500/50 border border-white/10 transition-all"
              >
                <div className="text-4xl mb-3">{symptom.icon}</div>
                <h3 className="text-xl font-bold mb-2">{symptom.title}</h3>
                <p className="text-gray-400">{symptom.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Find Nearby Hospitals */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="glass rounded-2xl p-8"
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-3xl font-bold flex items-center">
              <FaHospital className="mr-3 text-primary-500" />
              Nearby Hospitals
            </h2>
            <button
              onClick={getLocation}
              disabled={loading}
              className="px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-all hover:scale-105 disabled:opacity-50 disabled:hover:scale-100 flex items-center space-x-2"
            >
              <FaMapMarkerAlt />
              <span>{loading ? "Loading..." : "Find Hospitals"}</span>
            </button>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-900/20 border border-red-500 rounded-lg text-red-400">
              {error}
            </div>
          )}

          {location && (
            <div className="mb-6 p-4 bg-green-900/20 border border-green-500 rounded-lg text-green-400">
              <FaMapMarkerAlt className="inline mr-2" />
              Location detected: {location.lat.toFixed(4)},{" "}
              {location.lng.toFixed(4)}
            </div>
          )}

          {hospitals.length > 0 && (
            <div className="space-y-4">
              {hospitals.slice(0, 5).map((hospital, index) => (
                <motion.div
                  key={hospital.place_id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white/5 p-6 rounded-xl border border-white/10 hover:border-primary-500/50 transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold mb-2">
                        {hospital.name}
                      </h3>
                      <p className="text-gray-400 mb-2">{hospital.vicinity}</p>
                      <div className="flex items-center space-x-4 text-sm">
                        <span className="text-yellow-400">
                          ⭐ {hospital.rating} ({hospital.user_ratings_total}{" "}
                          reviews)
                        </span>
                      </div>
                    </div>
                    <a
                      href={`https://www.google.com/maps/search/?api=1&query=${hospital.lat},${hospital.lng}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-all hover:scale-105 flex items-center space-x-2"
                    >
                      <FaMapMarkerAlt />
                      <span>Directions</span>
                    </a>
                  </div>
                </motion.div>
              ))}
            </div>
          )}

          {!location && !loading && (
            <div className="text-center py-12">
              <FaHospital className="text-6xl text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">
                Click "Find Hospitals" to see nearby medical facilities
              </p>
            </div>
          )}
        </motion.div>

        {/* Important Note */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-8 text-center text-gray-500 text-sm"
        >
          <p>
            This tool is for informational purposes only. Always call emergency
            services for urgent medical situations.
          </p>
        </motion.div>
      </div>
    </div>
  );
}
