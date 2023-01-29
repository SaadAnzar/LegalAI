/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // CORS TO ALLOW ALL DOMAINS FOR FIREBASE
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Access-Control-Allow-Origin',
            value: '*',
          },
          {
            key: 'Access-Control-Allow-Methods',
            value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT',
          }
        ],
      },
    ]
  }
}

module.exports = nextConfig
