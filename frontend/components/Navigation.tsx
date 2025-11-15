"use client";

import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { FaHeartbeat, FaBars, FaTimes } from "react-icons/fa";
import { MdLocalHospital } from "react-icons/md";

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { name: "Home", href: "/" },
    { name: "Predict", href: "/predict" },
    { name: "Maps", href: "/maps" },
    { name: "Emergency", href: "/emergency" },
    { name: "About", href: "/about" },
  ];

  return (
    <nav className="fixed top-4 left-0 right-0 z-50 px-4">
      <div className="container mx-auto">
        <div className="glass rounded-2xl px-6 shadow-2xl border border-white/10">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link
              href="/"
              className="flex items-center space-x-2 text-2xl font-bold"
            >
              <MdLocalHospital className="text-primary-500 text-3xl" />
              <span className="bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                HealthAI
              </span>
            </Link>

            {/* Desktop Menu */}
            <div className="hidden md:flex items-center space-x-8">
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="text-gray-300 hover:text-primary-400 transition-colors font-medium"
                >
                  {item.name}
                </Link>
              ))}
              <Link
                href="/predict"
                className="px-6 py-2 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold transition-all hover:scale-105"
              >
                Get Started
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden text-2xl text-gray-300"
            >
              {isOpen ? <FaTimes /> : <FaBars />}
            </button>
          </div>

          {/* Mobile Menu */}
          {isOpen && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="md:hidden pb-6"
            >
              {navItems.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="block py-3 text-gray-300 hover:text-primary-400 transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
              <Link
                href="/predict"
                className="block mt-4 px-6 py-3 bg-primary-600 hover:bg-primary-700 rounded-lg font-semibold text-center transition-all"
                onClick={() => setIsOpen(false)}
              >
                Get Started
              </Link>
            </motion.div>
          )}
        </div>
      </div>
    </nav>
  );
}
