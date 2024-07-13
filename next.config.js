/** @type {import('next').NextConfig} */

const allowedImageHosts = [
  'img.daisyui.com',
  'via.placeholder.com',
  'images.unsplash.com',
  'cdn.shopify.com'
]

const nextConfig = {
  images: {
    remotePatterns: allowedImageHosts.map(
      (host) => (
        {
          hostname: host,
        }
      )
    )
  },
  experimental: {
    ppr: true,
  },
  transpilePackages: ["@tinyshop/tinyshop-node"]
}

module.exports = nextConfig