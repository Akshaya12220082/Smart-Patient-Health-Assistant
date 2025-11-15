/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  turbopack: {
    // ensure Turbopack resolves this frontend folder as the workspace root
    root: "./",
  },
};

module.exports = nextConfig;
