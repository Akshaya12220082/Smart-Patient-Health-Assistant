"use client";

import { motion } from "framer-motion";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";

interface RiskGaugeProps {
  score: number;
  zone?: "Green" | "Yellow" | "Red" | string;
  disease?: string;
}

export default function RiskGauge({
  score,
  zone = "Unknown",
  disease = "Health",
}: RiskGaugeProps) {
  const getZoneColor = (zone: string) => {
    switch (zone) {
      case "Green":
        return {
          bg: "bg-green-500/20",
          border: "border-green-500",
          text: "text-green-500",
          color: "#10b981",
        };
      case "Yellow":
        return {
          bg: "bg-yellow-500/20",
          border: "border-yellow-500",
          text: "text-yellow-500",
          color: "#f59e0b",
        };
      case "Red":
        return {
          bg: "bg-red-500/20",
          border: "border-red-500",
          text: "text-red-500",
          color: "#ef4444",
        };
      default:
        return {
          bg: "bg-gray-500/20",
          border: "border-gray-500",
          text: "text-gray-500",
          color: "#6b7280",
        };
    }
  };

  const zoneInfo = getZoneColor(zone);

  const data = [
    { name: "Risk", value: score },
    { name: "Safe", value: 100 - score },
  ];

  const getZoneMessage = () => {
    switch (zone) {
      case "Green":
        return {
          title: "Low Risk",
          message:
            "Your health indicators look good! Continue maintaining a healthy lifestyle.",
        };
      case "Yellow":
        return {
          title: "Moderate Risk",
          message:
            "Some risk factors detected. Consider consulting a healthcare professional and following our recommendations.",
        };
      case "Red":
        return {
          title: "High Risk",
          message:
            "Significant risk factors identified. We strongly recommend consulting a healthcare professional immediately.",
        };
      default:
        return {
          title: "Unknown",
          message: "Unable to determine risk level.",
        };
    }
  };

  const message = getZoneMessage();

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className={`glass p-8 rounded-2xl border-2 ${zoneInfo.border}`}
    >
      <h3 className="text-2xl font-bold mb-6 text-center">Risk Assessment</h3>

      {/* Gauge Chart */}
      <div className="relative">
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              startAngle={180}
              endAngle={0}
              innerRadius={60}
              outerRadius={80}
              paddingAngle={0}
              dataKey="value"
            >
              <Cell fill={zoneInfo.color} />
              <Cell fill="#1a1a1a" />
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        {/* Score Display */}
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/4 text-center">
          <div className={`text-5xl font-bold ${zoneInfo.text}`}>
            {Math.round(score)}%
          </div>
          <div className="text-gray-400 text-sm mt-1">Risk Score</div>
        </div>
      </div>

      {/* Zone Badge */}
      <div className="text-center mt-6">
        <span
          className={`inline-block px-6 py-2 ${zoneInfo.bg} ${zoneInfo.text} font-semibold rounded-full border ${zoneInfo.border}`}
        >
          {zone} Zone
        </span>
      </div>

      {/* Message */}
      <div className="mt-6 p-4 bg-dark-100 rounded-lg">
        <h4 className={`font-semibold mb-2 ${zoneInfo.text}`}>
          {message.title}
        </h4>
        <p className="text-gray-400 text-sm">{message.message}</p>
      </div>

      {/* Disease Info */}
      <div className="mt-4 text-center text-sm text-gray-500">
        {disease} Risk Assessment
      </div>
    </motion.div>
  );
}
