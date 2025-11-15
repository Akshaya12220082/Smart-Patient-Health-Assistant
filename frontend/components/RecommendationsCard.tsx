"use client";

import { motion } from "framer-motion";
import { RecommendationResponse } from "@/lib/api";
import {
  FaAppleAlt,
  FaRunning,
  FaStethoscope,
  FaClipboardList,
  FaHeartbeat,
} from "react-icons/fa";

interface RecommendationsCardProps {
  recommendations: RecommendationResponse | null | undefined;
}

export default function RecommendationsCard({
  recommendations,
}: RecommendationsCardProps) {
  if (!recommendations) {
    return null;
  }

  const sections = [
    {
      title: "Lifestyle Changes",
      icon: <FaHeartbeat className="w-5 h-5" />,
      items: recommendations.recommendations?.lifestyle || [],
      color: "text-blue-400",
    },
    {
      title: "Dietary Recommendations",
      icon: <FaAppleAlt className="w-5 h-5" />,
      items: recommendations.recommendations?.diet || [],
      color: "text-green-400",
    },
    {
      title: "Exercise Routine",
      icon: <FaRunning className="w-5 h-5" />,
      items: recommendations.recommendations?.exercise || [],
      color: "text-orange-400",
    },
    {
      title: "Health Monitoring",
      icon: <FaClipboardList className="w-5 h-5" />,
      items: recommendations.recommendations?.monitoring || [],
      color: "text-purple-400",
    },
    {
      title: "Medical Advice",
      icon: <FaStethoscope className="w-5 h-5" />,
      items: recommendations.recommendations?.medical || [],
      color: "text-red-400",
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass p-8 rounded-2xl"
    >
      <h3 className="text-2xl font-bold mb-6">Personalized Recommendations</h3>

      <div className="space-y-6">
        {sections.map(
          (section, index) =>
            section.items?.length > 0 && (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-dark-100 p-6 rounded-xl"
              >
                <div className="flex items-center space-x-3 mb-4">
                  <div className={section.color}>{section.icon}</div>
                  <h4 className="text-lg font-semibold">{section.title}</h4>
                </div>

                <ul className="space-y-3">
                  {section.items.map((item, i) => (
                    <li
                      key={i}
                      className="flex items-start space-x-3 text-gray-300"
                    >
                      <span className="text-primary-500 mt-1">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            )
        )}
      </div>

      <div className="mt-6 p-4 bg-yellow-900/20 border border-yellow-600 rounded-lg">
        <p className="text-yellow-400 text-sm">
          <strong>Disclaimer:</strong> These recommendations are based on AI
          analysis and should not replace professional medical advice. Please
          consult with a healthcare provider for personalized medical guidance.
        </p>
      </div>
    </motion.div>
  );
}
