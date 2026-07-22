import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* Proxy API calls to the FastAPI backend during development */
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/:path*`,
      },
    ];
  },
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/api/v1/files/**",
      },
    ],
  },
};

export default nextConfig;
