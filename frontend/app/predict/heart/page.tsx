"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import {
  predict,
  getRecommendations,
  PredictionResponse,
  RecommendationResponse,
} from "@/lib/api";
import RiskGauge from "@/components/RiskGauge";
import RecommendationsCard from "@/components/RecommendationsCard";

export default function HeartPrediction() {
  const [formData, setFormData] = useState({
    age: "",
    sex: "1",
    cp: "0",
    trestbps: "",
    chol: "",
    fbs: "0",
    restecg: "0",
    thalach: "",
    exang: "0",
    oldpeak: "",
    slope: "0",
    ca: "0",
    thal: "0",
  });

  const [prediction, setPrediction] = useState<PredictionResponse | null>(null);
  const [recommendations, setRecommendations] =
    useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setRecommendations(null);

    try {
      const data = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [key, parseFloat(value)])
      );
      console.log("🔍 Submitting heart prediction...");
      const predictionResult = await predict("heart", data);
      console.log("✅ Prediction result:", predictionResult);
      setPrediction(predictionResult);

      console.log("🔍 Fetching recommendations...");
      const recommendationsResult = await getRecommendations(
        "heart",
        predictionResult.risk_score
      );
      console.log("✅ Recommendations result:", recommendationsResult);
      setRecommendations(recommendationsResult);
    } catch (err: any) {
      const errorMessage =
        err?.response?.data?.error || err?.message || "Prediction failed";
      setError(errorMessage);
      console.error("❌ Error:", err);
      console.error("❌ Error details:", err?.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white py-20 px-4">
      <div className="max-w-4xl mx-auto">
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
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Heart Disease Prediction
          </h1>
          <p className="text-xl text-gray-400">
            Enter your health metrics for cardiovascular risk assessment
          </p>
        </motion.div>

        <motion.form
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          onSubmit={handleSubmit}
          className="bg-gradient-to-b from-primary-900/10 to-transparent border border-primary-800/30 rounded-2xl p-8 backdrop-blur-sm mb-8"
        >
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">Age</label>
              <input
                type="number"
                name="age"
                value={formData.age}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Sex</label>
              <select
                name="sex"
                value={formData.sex}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="1">Male</option>
                <option value="0">Female</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Chest Pain Type
              </label>
              <select
                name="cp"
                value={formData.cp}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">Typical Angina</option>
                <option value="1">Atypical Angina</option>
                <option value="2">Non-anginal Pain</option>
                <option value="3">Asymptomatic</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Resting Blood Pressure (mm Hg)
              </label>
              <input
                type="number"
                name="trestbps"
                value={formData.trestbps}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Cholesterol (mg/dl)
              </label>
              <input
                type="number"
                name="chol"
                value={formData.chol}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Fasting Blood Sugar {">"}120 mg/dl
              </label>
              <select
                name="fbs"
                value={formData.fbs}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Resting ECG Results
              </label>
              <select
                name="restecg"
                value={formData.restecg}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">Normal</option>
                <option value="1">ST-T Wave Abnormality</option>
                <option value="2">Left Ventricular Hypertrophy</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Maximum Heart Rate
              </label>
              <input
                type="number"
                name="thalach"
                value={formData.thalach}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Exercise Induced Angina
              </label>
              <select
                name="exang"
                value={formData.exang}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                ST Depression
              </label>
              <input
                type="number"
                step="0.1"
                name="oldpeak"
                value={formData.oldpeak}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Slope of Peak Exercise ST
              </label>
              <select
                name="slope"
                value={formData.slope}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">Upsloping</option>
                <option value="1">Flat</option>
                <option value="2">Downsloping</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Number of Major Vessels (0-3)
              </label>
              <select
                name="ca"
                value={formData.ca}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Thalassemia
              </label>
              <select
                name="thal"
                value={formData.thal}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">Normal</option>
                <option value="1">Fixed Defect</option>
                <option value="2">Reversible Defect</option>
              </select>
            </div>
          </div>

          {error && (
            <div className="mt-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="mt-8 w-full py-4 bg-primary-500 hover:bg-primary-600 rounded-lg text-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Analyzing..." : "Get Prediction"}
          </button>
        </motion.form>

        {prediction && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-6"
          >
            <RiskGauge
              score={prediction.risk_score}
              zone={prediction.zone}
              disease="Heart"
            />
            {recommendations && (
              <RecommendationsCard recommendations={recommendations} />
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
