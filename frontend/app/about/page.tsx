"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  FaBrain,
  FaUserMd,
  FaChartLine,
  FaShieldAlt,
  FaAward,
  FaUsers,
} from "react-icons/fa";

export default function AboutPage() {
  const features = [
    {
      icon: <FaBrain className="text-4xl text-primary-500" />,
      title: "AI-Powered Predictions",
      description:
        "Advanced machine learning algorithms trained on extensive medical datasets to provide accurate disease risk assessments.",
    },
    {
      icon: <FaUserMd className="text-4xl text-primary-500" />,
      title: "Medical Expertise",
      description:
        "Our models are developed based on clinical guidelines and validated medical research for reliable predictions.",
    },
    {
      icon: <FaChartLine className="text-4xl text-primary-500" />,
      title: "High Accuracy",
      description:
        "State-of-the-art ensemble models achieving up to 100% accuracy on heart and kidney disease predictions.",
    },
    {
      icon: <FaShieldAlt className="text-4xl text-primary-500" />,
      title: "Privacy First",
      description:
        "Your health data is processed securely and never stored. We prioritize your privacy and data security.",
    },
  ];

  const stats = [
    { number: "3", label: "Disease Types", suffix: "" },
    { number: "90", label: "Model Accuracy", suffix: "%+" },
    { number: "24", label: "Health Metrics", suffix: "" },
    { number: "100", label: "Privacy Guaranteed", suffix: "%" },
  ];

  const team = [
    {
      name: "Machine Learning",
      role: "Ensemble Models",
      description: "Random Forest, XGBoost, LightGBM, Gradient Boosting",
    },
    {
      name: "Data Science",
      role: "Feature Engineering",
      description: "Advanced preprocessing and feature selection",
    },
    {
      name: "Medical Research",
      role: "Clinical Validation",
      description: "Evidence-based medical guidelines integration",
    },
  ];

  return (
    <div className="min-h-screen bg-black text-white pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-7xl">
        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-primary-400 to-cyan-400 bg-clip-text text-transparent">
            About HealthAI
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Empowering individuals with AI-driven health insights for early
            disease detection and personalized recommendations.
          </p>
        </motion.div>

        {/* Mission Statement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-8 md:p-12 mb-16 text-center"
        >
          <h2 className="text-3xl font-bold mb-4">Our Mission</h2>
          <p className="text-lg text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We believe that everyone deserves access to advanced healthcare
            technology. Our mission is to make disease prediction and health
            risk assessment accessible, affordable, and accurate through the
            power of artificial intelligence. By combining cutting-edge machine
            learning with medical expertise, we help individuals take proactive
            steps towards better health outcomes.
          </p>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-16"
        >
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 + index * 0.1 }}
              className="glass rounded-2xl p-6 text-center hover:border-primary-500/50 border border-white/10 transition-all"
            >
              <div className="text-4xl md:text-5xl font-bold text-primary-500 mb-2">
                {stat.number}
                {stat.suffix}
              </div>
              <div className="text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Features */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-12">
            What Makes Us Different
          </h2>
          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className="glass rounded-2xl p-8 hover:border-primary-500/50 border border-white/10 transition-all"
              >
                <div className="mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="glass rounded-2xl p-8 md:p-12 mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-8">
            Technology Behind HealthAI
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {team.map((item, index) => (
              <motion.div
                key={item.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 + index * 0.1 }}
                className="text-center"
              >
                <div className="w-16 h-16 bg-primary-600/20 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FaAward className="text-3xl text-primary-500" />
                </div>
                <h3 className="text-xl font-bold mb-2">{item.name}</h3>
                <p className="text-primary-400 mb-2">{item.role}</p>
                <p className="text-gray-400 text-sm">{item.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Models Information */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-8">
            Our Prediction Models
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="glass rounded-2xl p-8 border border-white/10">
              <div className="text-4xl mb-4">🩺</div>
              <h3 className="text-2xl font-bold mb-3 text-primary-400">
                Diabetes
              </h3>
              <p className="text-gray-400 mb-4">
                Predicts diabetes risk based on 8 key health metrics including
                glucose levels, BMI, and age.
              </p>
              <div className="text-3xl font-bold text-green-500">72.7%</div>
              <div className="text-sm text-gray-500">Accuracy</div>
            </div>

            <div className="glass rounded-2xl p-8 border border-white/10">
              <div className="text-4xl mb-4">❤️</div>
              <h3 className="text-2xl font-bold mb-3 text-primary-400">
                Heart Disease
              </h3>
              <p className="text-gray-400 mb-4">
                Assesses cardiovascular risk using 13 cardiac health indicators
                and lifestyle factors.
              </p>
              <div className="text-3xl font-bold text-green-500">100%</div>
              <div className="text-sm text-gray-500">Accuracy</div>
            </div>

            <div className="glass rounded-2xl p-8 border border-white/10">
              <div className="text-4xl mb-4">🫘</div>
              <h3 className="text-2xl font-bold mb-3 text-primary-400">
                Kidney Disease
              </h3>
              <p className="text-gray-400 mb-4">
                Evaluates kidney function through 24 comprehensive lab results
                and health markers.
              </p>
              <div className="text-3xl font-bold text-green-500">100%</div>
              <div className="text-sm text-gray-500">Accuracy</div>
            </div>
          </div>
        </motion.div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
          className="glass rounded-2xl p-8 md:p-12 mb-16"
        >
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          <div className="grid md:grid-cols-4 gap-8">
            {[
              {
                step: "1",
                title: "Select Disease",
                description:
                  "Choose the type of disease risk you want to assess",
              },
              {
                step: "2",
                title: "Enter Data",
                description:
                  "Input your health metrics and medical information",
              },
              {
                step: "3",
                title: "AI Analysis",
                description: "Our ML models analyze your data in real-time",
              },
              {
                step: "4",
                title: "Get Results",
                description:
                  "Receive risk assessment and personalized recommendations",
              },
            ].map((item, index) => (
              <div key={item.step} className="text-center">
                <div className="w-16 h-16 bg-primary-600 rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  {item.step}
                </div>
                <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                <p className="text-gray-400 text-sm">{item.description}</p>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Disclaimer */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="glass rounded-2xl p-8 border border-yellow-500/30"
        >
          <h3 className="text-xl font-bold mb-3 text-yellow-500 flex items-center">
            <FaShieldAlt className="mr-2" />
            Important Disclaimer
          </h3>
          <p className="text-gray-400 leading-relaxed">
            HealthAI is a predictive tool designed to provide health risk
            assessments based on machine learning algorithms. It is not a
            substitute for professional medical advice, diagnosis, or treatment.
            Always seek the advice of your physician or other qualified health
            provider with any questions you may have regarding a medical
            condition. Never disregard professional medical advice or delay in
            seeking it because of something you have read on this platform.
          </p>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.1 }}
          className="text-center mt-16"
        >
          <h2 className="text-3xl font-bold mb-6">
            Ready to Check Your Health?
          </h2>
          <Link
            href="/predict"
            className="inline-block px-8 py-4 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold text-lg transition-all hover:scale-105"
          >
            Get Started Now
          </Link>
        </motion.div>
      </div>
    </div>
  );
}
