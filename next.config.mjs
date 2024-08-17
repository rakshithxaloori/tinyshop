/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "cosmix.in",
      },
      {
        protocol: "https",
        hostname: "vercel.com",
      }
    ],
  },
  transpilePackages: ["@tinyshop/tinyshop-node"],
};

export default nextConfig;
