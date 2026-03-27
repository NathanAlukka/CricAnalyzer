import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef7f2",
          100: "#d6ecdf",
          500: "#2f7d4f",
          700: "#1f5f39",
          900: "#153d26",
        },
      },
    },
  },
  plugins: [],
};

export default config;
