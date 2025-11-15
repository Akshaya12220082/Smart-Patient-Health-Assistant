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

export default function KidneyPrediction() {
  const [formData, setFormData] = useState({
    age: "",
    bp: "",
    sg: "1.020",
    al: "0",
    su: "0",
    rbc: "1",
    pc: "0",
    pcc: "0",
    ba: "0",
    bgr: "",
    bu: "",
    sc: "",
    sod: "",
    pot: "",
    hemo: "",
    pcv: "",
    wc: "",
    rc: "",
    htn: "0",
    dm: "0",
    cad: "0",
    appet: "1",
    pe: "0",
    ane: "0",
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
      console.log("🔍 Submitting kidney prediction...");
      const predictionResult = await predict("kidney", data);
      console.log("✅ Prediction result:", predictionResult);
      setPrediction(predictionResult);

      console.log("🔍 Fetching recommendations...");
      const recommendationsResult = await getRecommendations(
        "kidney",
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
            Kidney Disease Prediction
          </h1>
          <p className="text-xl text-gray-400">
            Enter your health metrics for kidney function assessment
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
              <label className="block text-sm font-medium mb-2">
                Blood Pressure (mm Hg)
              </label>
              <input
                type="number"
                name="bp"
                value={formData.bp}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Specific Gravity
              </label>
              <select
                name="sg"
                value={formData.sg}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="1.005">1.005</option>
                <option value="1.010">1.010</option>
                <option value="1.015">1.015</option>
                <option value="1.020">1.020</option>
                <option value="1.025">1.025</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Albumin (0-5)
              </label>
              <input
                type="number"
                name="al"
                value={formData.al}
                onChange={handleChange}
                required
                min="0"
                max="5"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Sugar (0-5)
              </label>
              <input
                type="number"
                name="su"
                value={formData.su}
                onChange={handleChange}
                required
                min="0"
                max="5"
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Red Blood Cells
              </label>
              <select
                name="rbc"
                value={formData.rbc}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="1">Normal</option>
                <option value="0">Abnormal</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Pus Cell</label>
              <select
                name="pc"
                value={formData.pc}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">Normal</option>
                <option value="1">Abnormal</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Blood Glucose Random (mg/dl)
              </label>
              <input
                type="number"
                name="bgr"
                value={formData.bgr}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Blood Urea (mg/dl)
              </label>
              <input
                type="number"
                name="bu"
                value={formData.bu}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Serum Creatinine (mg/dl)
              </label>
              <input
                type="number"
                step="0.1"
                name="sc"
                value={formData.sc}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Sodium (mEq/L)
              </label>
              <input
                type="number"
                name="sod"
                value={formData.sod}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Potassium (mEq/L)
              </label>
              <input
                type="number"
                step="0.1"
                name="pot"
                value={formData.pot}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Hemoglobin (g)
              </label>
              <input
                type="number"
                step="0.1"
                name="hemo"
                value={formData.hemo}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Packed Cell Volume
              </label>
              <input
                type="number"
                name="pcv"
                value={formData.pcv}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                White Blood Cell Count
              </label>
              <input
                type="number"
                name="wc"
                value={formData.wc}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Red Blood Cell Count
              </label>
              <input
                type="number"
                step="0.1"
                name="rc"
                value={formData.rc}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Hypertension
              </label>
              <select
                name="htn"
                value={formData.htn}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Diabetes Mellitus
              </label>
              <select
                name="dm"
                value={formData.dm}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Appetite</label>
              <select
                name="appet"
                value={formData.appet}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="1">Good</option>
                <option value="0">Poor</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Anemia</label>
              <select
                name="ane"
                value={formData.ane}
                onChange={handleChange}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500"
              >
                <option value="0">No</option>
                <option value="1">Yes</option>
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
              disease="Kidney"
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
