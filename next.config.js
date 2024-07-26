/** @type {import('next').NextConfig} */

const allowedImageHosts = [
  'img.daisyui.com',
  'via.placeholder.com',
  'images.unsplash.com',
  'cdn.shopify.com',
  'plus.unsplash.com',
  'cosmix.in'
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
    ppr: 'incremental',
  },
  transpilePackages: ["@tinyshop/tinyshop-node"]
}

module.exports = nextConfig