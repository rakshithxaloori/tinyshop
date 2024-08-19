/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "ts-storefront-images.s3.ap-south-1.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "vercel.com",
      },
    ],
  },
  transpilePackages: ["@tinyshop/tinyshop-node"],
};

export default nextConfig;
