/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [],
  },
  transpilePackages: ["@tinyshop/tinyshop-node"],
};

export default nextConfig;
