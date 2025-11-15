"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { FaHeartbeat, FaTint } from "react-icons/fa";
import { GiKidneys } from "react-icons/gi";

export default function PredictPage() {
  const diseases = [
    {
      name: "Diabetes",
      icon: <FaTint className="w-16 h-16" />,
      description:
        "Predict your risk of developing Type 2 Diabetes based on key health indicators",
      color: "from-blue-500 to-cyan-500",
      href: "/predict/diabetes",
    },
    {
      name: "Heart Disease",
      icon: <FaHeartbeat className="w-16 h-16" />,
      description:
        "Assess your cardiovascular health and risk of heart-related conditions",
      color: "from-red-500 to-pink-500",
      href: "/predict/heart",
    },
    {
      name: "Kidney Disease",
      icon: <GiKidneys className="w-16 h-16" />,
      description:
        "Evaluate kidney function and detect early signs of chronic kidney disease",
      color: "from-purple-500 to-indigo-500",
      href: "/predict/kidney",
    },
  ];

  return (
    <div className="min-h-screen bg-black text-white pt-32 pb-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Health Risk Prediction
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Select a disease category to get started with your personalized
            health assessment. Our AI-powered models analyze your health data to
            provide accurate risk predictions.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {diseases.map((disease, index) => (
            <motion.div
              key={disease.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.2 }}
            >
              <Link href={disease.href}>
                <div className="glass p-8 rounded-2xl card-hover h-full cursor-pointer group">
                  <div
                    className={`bg-gradient-to-r ${disease.color} p-4 rounded-xl inline-block mb-6 group-hover:scale-110 transition-transform`}
                  >
                    <div className="text-white">{disease.icon}</div>
                  </div>
                  <h3 className="text-2xl font-bold mb-4">{disease.name}</h3>
                  <p className="text-gray-400 mb-6">{disease.description}</p>
                  <div className="flex items-center text-primary-500 font-semibold group-hover:translate-x-2 transition-transform">
                    Start Assessment
                    <svg
                      className="w-5 h-5 ml-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 5l7 7-7 7"
                      />
                    </svg>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          className="mt-16 text-center"
        >
          <div className="glass p-8 rounded-2xl max-w-4xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">How It Works</h3>
            <div className="grid md:grid-cols-3 gap-6 mt-8">
              <div>
                <div className="text-4xl font-bold text-primary-500 mb-2">
                  1
                </div>
                <h4 className="font-semibold mb-2">Input Health Data</h4>
                <p className="text-gray-400 text-sm">
                  Provide your health metrics and medical history
                </p>
              </div>
              <div>
                <div className="text-4xl font-bold text-primary-500 mb-2">
                  2
                </div>
                <h4 className="font-semibold mb-2">AI Analysis</h4>
                <p className="text-gray-400 text-sm">
                  Our models analyze patterns and risk factors
                </p>
              </div>
              <div>
                <div className="text-4xl font-bold text-primary-500 mb-2">
                  3
                </div>
                <h4 className="font-semibold mb-2">Get Results</h4>
                <p className="text-gray-400 text-sm">
                  Receive personalized recommendations and insights
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
