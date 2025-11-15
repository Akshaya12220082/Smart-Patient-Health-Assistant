"use client";

import Link from "next/link";
import { FaGithub, FaLinkedin, FaTwitter, FaEnvelope } from "react-icons/fa";
import { MdLocalHospital } from "react-icons/md";

export default function Footer() {
  return (
    <footer className="bg-dark-200 border-t border-gray-900">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <MdLocalHospital className="text-primary-500 text-3xl" />
              <span className="text-2xl font-bold bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                HealthAI
              </span>
            </div>
            <p className="text-gray-400 mb-4 max-w-md">
              AI-powered healthcare predictions to help you stay ahead of health
              risks. Early detection saves lives.
            </p>
            <div className="flex space-x-4">
              <a
                href="#"
                className="text-gray-400 hover:text-primary-500 transition-colors"
              >
                <FaGithub className="text-2xl" />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-primary-500 transition-colors"
              >
                <FaLinkedin className="text-2xl" />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-primary-500 transition-colors"
              >
                <FaTwitter className="text-2xl" />
              </a>
              <a
                href="#"
                className="text-gray-400 hover:text-primary-500 transition-colors"
              >
                <FaEnvelope className="text-2xl" />
              </a>
            </div>
          </div>

          {/* Menu */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Menu</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/predict"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Predict
                </Link>
              </li>
              <li>
                <Link
                  href="/emergency"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Emergency
                </Link>
              </li>
              <li>
                <Link
                  href="/about"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  About
                </Link>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Services</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/predict/diabetes"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Diabetes
                </Link>
              </li>
              <li>
                <Link
                  href="/predict/heart"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Heart Disease
                </Link>
              </li>
              <li>
                <Link
                  href="/predict/kidney"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Kidney Disease
                </Link>
              </li>
              <li>
                <Link
                  href="/emergency"
                  className="text-gray-400 hover:text-primary-500 transition-colors"
                >
                  Emergency SOS
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-400">
          <p>
            &copy; {new Date().getFullYear()} Smart Patient Health Assistant.
            All rights reserved.
          </p>
          <p className="mt-2 text-sm">
            Built with ❤️ using Next.js, React & AI
          </p>
        </div>
      </div>
    </footer>
  );
}
