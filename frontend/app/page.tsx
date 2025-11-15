"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import {
  FaHeartbeat,
  FaShieldAlt,
  FaChartLine,
  FaBrain,
  FaUserMd,
  FaAward,
} from "react-icons/fa";
import {
  MdLocalHospital,
  MdEmail,
  MdPhone,
  MdLocationOn,
} from "react-icons/md";
import { SiTensorflow, SiPython, SiScikitlearn } from "react-icons/si";
import { useState } from "react";

export default function Home() {
  const [contactForm, setContactForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phone: "",
    message: "",
  });

  const handleContactSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Contact form submitted:", contactForm);
    // Handle form submission
  };

  return (
    <div className="bg-black text-white">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        {/* Curved background element */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute bottom-0 left-0 right-0 h-96 bg-gradient-to-t from-gray-900/50 to-transparent rounded-t-[50%]"></div>
        </div>

        {/* Animated background */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-primary-700/10 rounded-full blur-3xl animate-pulse delay-700"></div>
        </div>

        <div className="relative z-10 text-center px-4 max-w-6xl mx-auto py-20">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="inline-block px-6 py-2 mb-8 text-sm font-medium text-gray-300 bg-white/5 rounded-full border border-white/10 backdrop-blur-sm">
              🏥 Health Intelligence
            </span>
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              Empower Your Health with{" "}
              <span className="bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                AI-Powered
              </span>
              <br />
              Disease Predictions!
            </h1>
            <p className="text-lg md:text-xl text-gray-400 mb-10 max-w-3xl mx-auto">
              Get instant, accurate health risk assessments using advanced
              machine learning. Early detection saves lives—discover your health
              insights today.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link href="/predict">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-white text-black hover:bg-gray-200 rounded-full text-base font-semibold transition-all"
                >
                  Get Started
                </motion.button>
              </Link>
              <Link href="#features">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-8 py-4 bg-transparent hover:bg-white/10 rounded-full text-base font-semibold transition-all border border-white/20"
                >
                  Learn More
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Partners Section */}
      <section className="py-16 px-4 bg-gradient-to-b from-transparent to-gray-900/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <p className="text-sm text-gray-400 mb-8">Powered By</p>
            <p className="text-gray-400 text-base max-w-2xl mx-auto mb-12">
              Built with cutting-edge machine learning frameworks and medical AI
              technologies
            </p>
          </motion.div>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            {[
              {
                name: "TensorFlow",
                icon: <SiTensorflow className="text-4xl" />,
              },
              { name: "Python", icon: <SiPython className="text-4xl" /> },
              {
                name: "Scikit-Learn",
                icon: <SiScikitlearn className="text-4xl" />,
              },
              { name: "Medical AI", icon: <FaBrain className="text-4xl" /> },
              { name: "Healthcare", icon: <FaUserMd className="text-4xl" /> },
            ].map((partner, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="flex flex-col items-center justify-center p-8 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 transition-all"
              >
                {partner.icon}
                <p className="mt-3 text-sm text-gray-400">{partner.name}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section
        id="features"
        className="py-24 px-4 bg-gradient-to-b from-gray-900/30 to-black"
      >
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <p className="text-sm text-gray-400 mb-4">Why Choose Us</p>
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Advanced Health Analytics Platform
            </h2>
            <p className="text-lg text-gray-400 max-w-3xl mx-auto">
              Experience the future of preventive healthcare with our
              state-of-the-art AI models trained on extensive medical datasets
              for accurate disease risk predictions.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="p-10 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm hover:border-primary-500/50 transition-all group"
            >
              <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-primary-500/20 transition-all">
                <FaShieldAlt className="text-3xl text-primary-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Trusted</h3>
              <p className="text-gray-400 leading-relaxed">
                Built on validated medical research and trained on thousands of
                patient records with strict privacy compliance and data
                security.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="p-10 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm hover:border-primary-500/50 transition-all group"
            >
              <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-primary-500/20 transition-all">
                <FaHeartbeat className="text-3xl text-primary-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Accurate</h3>
              <p className="text-gray-400 leading-relaxed">
                Our machine learning models achieve over 90% accuracy in disease
                prediction, validated through rigorous testing and
                cross-validation.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="p-10 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm hover:border-primary-500/50 transition-all group"
            >
              <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-primary-500/20 transition-all">
                <FaChartLine className="text-3xl text-primary-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4">Comprehensive</h3>
              <p className="text-gray-400 leading-relaxed">
                Get personalized health recommendations, lifestyle
                modifications, and actionable insights tailored to your unique
                health profile.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="py-24 px-4 bg-black">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Health Prediction Services
            </h2>
            <p className="text-lg text-gray-400 max-w-3xl mx-auto">
              Choose from our comprehensive range of AI-powered disease
              prediction services. Each includes detailed risk analysis and
              personalized health recommendations.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {/* Basic Package */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="p-8 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm hover:border-primary-500/50 transition-all"
            >
              <div className="mb-8">
                <div className="inline-block px-4 py-2 bg-red-500/20 rounded-full text-sm font-medium mb-4">
                  🩺 Diabetes Risk Assessment
                </div>
                <h3 className="text-2xl font-bold mb-2">
                  Comprehensive Analysis
                </h3>
                <p className="text-gray-400 text-sm mb-2">
                  • Blood glucose level evaluation
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • BMI and lifestyle factors
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Family history assessment
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Pregnancy history (if applicable)
                </p>
                <p className="text-gray-400 text-sm mb-6">
                  • Personalized prevention strategies
                </p>
                <div className="text-3xl font-bold mb-2">
                  <span className="text-primary-400">Instant Results</span>
                </div>
              </div>
              <Link href="/predict/diabetes">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="w-full py-4 bg-white/10 hover:bg-white/20 rounded-full font-semibold transition-all border border-white/20"
                >
                  Get Started
                </motion.button>
              </Link>
            </motion.div>

            {/* Standard Package */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="p-8 rounded-3xl bg-gradient-to-b from-primary-900/20 to-transparent border border-primary-500/50 backdrop-blur-sm relative"
            >
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <span className="px-4 py-1 bg-primary-500 text-white text-xs font-bold rounded-full">
                  POPULAR
                </span>
              </div>
              <div className="mb-8">
                <div className="inline-block px-4 py-2 bg-primary-500/20 rounded-full text-sm font-medium mb-4">
                  ❤️ Heart Disease Prediction
                </div>
                <h3 className="text-2xl font-bold mb-2">
                  Cardiovascular Risk Analysis
                </h3>
                <p className="text-gray-400 text-sm mb-2">
                  • Blood pressure monitoring
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Cholesterol level assessment
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • ECG analysis interpretation
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Age and lifestyle factors
                </p>
                <p className="text-gray-400 text-sm mb-6">
                  • Heart-healthy lifestyle recommendations
                </p>
                <div className="text-3xl font-bold mb-2">
                  <span className="text-primary-400">Instant Results</span>
                </div>
              </div>
              <Link href="/predict/heart">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="w-full py-4 bg-primary-500 hover:bg-primary-600 rounded-full font-semibold transition-all"
                >
                  Get Started
                </motion.button>
              </Link>
            </motion.div>

            {/* Premium Package */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.3 }}
              className="p-8 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm hover:border-primary-500/50 transition-all"
            >
              <div className="mb-8">
                <div className="inline-block px-4 py-2 bg-green-500/20 rounded-full text-sm font-medium mb-4">
                  🫘 Kidney Disease Prediction
                </div>
                <h3 className="text-2xl font-bold mb-2">
                  Renal Function Assessment
                </h3>
                <p className="text-gray-400 text-sm mb-2">
                  • Serum creatinine levels
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Blood urea analysis
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Hemoglobin and RBC count
                </p>
                <p className="text-gray-400 text-sm mb-2">
                  • Hypertension and diabetes factors
                </p>
                <p className="text-gray-400 text-sm mb-6">
                  • Kidney-friendly diet recommendations
                </p>
                <div className="text-3xl font-bold mb-2">
                  <span className="text-primary-400">Instant Results</span>
                </div>
              </div>
              <Link href="/predict/kidney">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  className="w-full py-4 bg-white/10 hover:bg-white/20 rounded-full font-semibold transition-all border border-white/20"
                >
                  Get Started
                </motion.button>
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Projects Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-black to-gray-900/30">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Success Stories
            </h2>
            <p className="text-lg text-gray-400 max-w-2xl">
              Real people using our AI-powered predictions for early disease
              detection and preventive healthcare. Your health journey starts
              here.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {[
              {
                title: "Early Diabetes Detection & Management",
                category: "Diabetes Prevention",
                image: "bg-gradient-to-br from-red-900/40 to-red-600/20",
                description:
                  "Identified pre-diabetic conditions early, enabling lifestyle changes",
              },
              {
                title: "Cardiovascular Risk Assessment Success",
                category: "Heart Health",
                image: "bg-gradient-to-br from-blue-900/40 to-blue-600/20",
                description:
                  "Accurate heart disease risk prediction led to timely intervention",
              },
              {
                title: "Kidney Function Monitoring & Care",
                category: "Renal Health",
                image: "bg-gradient-to-br from-green-900/40 to-green-600/20",
                description:
                  "Early chronic kidney disease detection improved patient outcomes",
              },
              {
                title: "Comprehensive Health Analytics Platform",
                category: "Preventive Care",
                image: "bg-gradient-to-br from-purple-900/40 to-purple-600/20",
                description:
                  "Holistic health monitoring with personalized recommendations",
              },
            ].map((project, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="group cursor-pointer"
              >
                <div
                  className={`${project.image} h-64 rounded-3xl mb-6 border border-white/10 backdrop-blur-sm overflow-hidden relative group-hover:border-primary-500/50 transition-all`}
                >
                  <div className="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-all"></div>
                  <div className="absolute top-6 right-6">
                    <span className="px-3 py-1 bg-white/10 backdrop-blur-sm rounded-full text-xs font-medium border border-white/20">
                      {project.category}
                    </span>
                  </div>
                </div>
                <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                  {project.title}
                </h3>
                <p className="text-gray-400 text-sm">{project.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-24 px-4 bg-gradient-to-b from-gray-900/30 to-black">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Get In Touch
            </h2>
            <p className="text-lg text-gray-400 max-w-3xl mx-auto">
              Have questions about our health prediction services? Need support
              with your health assessment? Our team is here to help you on your
              journey to better health.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12">
            {/* Contact Form */}
            <motion.form
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              onSubmit={handleContactSubmit}
              className="space-y-6"
            >
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">
                    First Name
                  </label>
                  <input
                    type="text"
                    value={contactForm.firstName}
                    onChange={(e) =>
                      setContactForm({
                        ...contactForm,
                        firstName: e.target.value,
                      })
                    }
                    className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500 transition-all"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2 text-gray-300">
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={contactForm.lastName}
                    onChange={(e) =>
                      setContactForm({
                        ...contactForm,
                        lastName: e.target.value,
                      })
                    }
                    className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500 transition-all"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Email Address
                </label>
                <input
                  type="email"
                  value={contactForm.email}
                  onChange={(e) =>
                    setContactForm({ ...contactForm, email: e.target.value })
                  }
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500 transition-all"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Phone Number
                </label>
                <input
                  type="tel"
                  value={contactForm.phone}
                  onChange={(e) =>
                    setContactForm({ ...contactForm, phone: e.target.value })
                  }
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500 transition-all"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2 text-gray-300">
                  Message
                </label>
                <textarea
                  value={contactForm.message}
                  onChange={(e) =>
                    setContactForm({ ...contactForm, message: e.target.value })
                  }
                  rows={6}
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg focus:outline-none focus:border-primary-500 transition-all resize-none"
                  required
                />
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                type="submit"
                className="w-full py-4 bg-primary-500 hover:bg-primary-600 rounded-lg font-semibold transition-all"
              >
                Send Now
              </motion.button>
            </motion.form>

            {/* Contact Info */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <div className="p-8 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                    <MdEmail className="text-xl text-primary-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Email</h3>
                    <p className="text-gray-400">support@healthpredict.ai</p>
                    <p className="text-gray-400">help@healthpredict.ai</p>
                  </div>
                </div>
              </div>

              <div className="p-8 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                    <MdPhone className="text-xl text-primary-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Phone</h3>
                    <p className="text-gray-400">+1 (800) HEALTH-AI</p>
                    <p className="text-gray-400">+1 (800) 432-5841</p>
                  </div>
                </div>
              </div>

              <div className="p-8 rounded-3xl bg-gradient-to-b from-white/5 to-transparent border border-white/10 backdrop-blur-sm">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-primary-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                    <MdLocationOn className="text-xl text-primary-400" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold mb-2">Location</h3>
                    <p className="text-gray-400">Medical AI Center</p>
                    <p className="text-gray-400">San Francisco, CA 94102</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  );
}
