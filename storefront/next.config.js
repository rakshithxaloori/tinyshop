/** @type {import('next').NextConfig} */

const allowedImageHosts = [
  'img.daisyui.com',
  'via.placeholder.com',
  'images.unsplash.com',
  'cdn.shopify.com',
  'plus.unsplash.com',
  'cosmix.in',
  'tailwindui.com',
  "ts-storefront-images.s3.ap-south-1.amazonaws.com",
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
  // Error: ENOENT: no such file or directory, open '/vercel/path0/.next/server/app/index.rsc'
  // https://github.com/orgs/vercel/discussions/6981
  // Fix is to disable experimental ppr
  // experimental: {
  //   ppr: 'incremental',
  // },
  transpilePackages: ["@tinyshop/tinyshop-node"]
}

module.exports = nextConfig