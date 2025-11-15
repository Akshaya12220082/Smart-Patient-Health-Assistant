"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  healthAPI,
  PredictionResponse,
  RecommendationResponse,
} from "@/lib/api";
import RiskGauge from "@/components/RiskGauge";
import RecommendationsCard from "@/components/RecommendationsCard";

interface DiabetesFormData {
  Pregnancies: number;
  Glucose: number;
  BloodPressure: number;
  SkinThickness: number;
  Insulin: number;
  BMI: number;
  DiabetesPedigreeFunction: number;
  Age: number;
}

export default function DiabetesPage() {
  const [formData, setFormData] = useState<DiabetesFormData>({
    Pregnancies: 0,
    Glucose: 100,
    BloodPressure: 80,
    SkinThickness: 20,
    Insulin: 80,
    BMI: 25,
    DiabetesPedigreeFunction: 0.5,
    Age: 30,
  });

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [recommendations, setRecommendations] =
    useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: parseFloat(value) || 0,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRecommendations(null);

    try {
      console.log("🔍 Submitting prediction...");
      const predictionResult = await healthAPI.predict("diabetes", formData);
      console.log("✅ Prediction result:", predictionResult);
      setPrediction(predictionResult);

      console.log("🔍 Fetching recommendations...");
      const recommendationsResult = await healthAPI.getRecommendations(
        "diabetes",
        predictionResult.risk_score
      );
      console.log("✅ Recommendations result:", recommendationsResult);
      setRecommendations(recommendationsResult);
    } catch (err: any) {
      const errorMessage =
        err?.response?.data?.error ||
        err?.message ||
        "Failed to get prediction";
      setError(errorMessage);
      console.error("❌ Error:", err);
      console.error("❌ Error details:", err?.response?.data);
    } finally {
      setLoading(false);
    }
  };

  const formFields = [
    {
      name: "Pregnancies",
      label: "Number of Pregnancies",
      min: 0,
      max: 20,
      step: 1,
    },
    {
      name: "Glucose",
      label: "Glucose Level (mg/dL)",
      min: 0,
      max: 300,
      step: 1,
    },
    {
      name: "BloodPressure",
      label: "Blood Pressure (mm Hg)",
      min: 0,
      max: 200,
      step: 1,
    },
    {
      name: "SkinThickness",
      label: "Skin Thickness (mm)",
      min: 0,
      max: 100,
      step: 1,
    },
    {
      name: "Insulin",
      label: "Insulin Level (μU/mL)",
      min: 0,
      max: 900,
      step: 1,
    },
    { name: "BMI", label: "BMI (Body Mass Index)", min: 0, max: 70, step: 0.1 },
    {
      name: "DiabetesPedigreeFunction",
      label: "Diabetes Pedigree Function",
      min: 0,
      max: 2.5,
      step: 0.001,
    },
    { name: "Age", label: "Age (years)", min: 1, max: 120, step: 1 },
  ];

  return (
    <div className="min-h-screen bg-black text-white pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-7xl">
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Link
            href="/predict"
            className="inline-flex items-center space-x-2 text-gray-400 hover:text-primary-400 transition-colors group"
          >
            <svg
              className="w-5 h-5 transform group-hover:-translate-x-1 transition-transform"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
            <span>Back to Disease Selection</span>
          </Link>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Diabetes Risk Assessment
          </h1>
          <p className="text-xl text-gray-400">
            Enter your health metrics to assess your diabetes risk
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass p-8 rounded-2xl"
          >
            <h2 className="text-2xl font-bold mb-6">Health Metrics</h2>
            <form onSubmit={handleSubmit} className="space-y-6">
              {formFields.map((field) => (
                <div key={field.name}>
                  <label className="block text-sm font-medium mb-2">
                    {field.label}
                  </label>
                  <div className="flex items-center space-x-4">
                    <input
                      type="range"
                      name={field.name}
                      min={field.min}
                      max={field.max}
                      step={field.step}
                      value={formData[field.name as keyof DiabetesFormData]}
                      onChange={handleInputChange}
                      className="flex-1 h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-primary-500"
                    />
                    <input
                      type="number"
                      name={field.name}
                      min={field.min}
                      max={field.max}
                      step={field.step}
                      value={formData[field.name as keyof DiabetesFormData]}
                      onChange={handleInputChange}
                      className="w-24 px-3 py-2 bg-dark-100 border border-gray-700 rounded-lg focus:outline-none focus:border-primary-500"
                    />
                  </div>
                </div>
              ))}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold text-lg transition-all hover:scale-105 disabled:opacity-50 disabled:hover:scale-100"
              >
                {loading ? "Analyzing..." : "Get Prediction"}
              </button>

              {error && (
                <div className="p-4 bg-red-900/20 border border-red-500 rounded-lg text-red-400">
                  {error}
                </div>
              )}
            </form>
          </motion.div>

          {/* Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {prediction ? (
              <>
                <RiskGauge
                  score={prediction.risk_score}
                  zone={prediction.zone}
                  disease="Diabetes"
                />
                {recommendations && (
                  <RecommendationsCard recommendations={recommendations} />
                )}
              </>
            ) : (
              <div className="glass p-12 rounded-2xl text-center">
                <div className="text-6xl mb-4">🩺</div>
                <h3 className="text-xl font-semibold mb-2">Ready to Analyze</h3>
                <p className="text-gray-400">
                  Fill in your health metrics and click "Get Prediction" to see
                  your risk assessment
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
}
