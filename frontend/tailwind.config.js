/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontSize: {
        xs: ['0.625rem', '0.875rem'],  // 10px
        sm: ['0.75rem', '1rem'],       // 12px
        base: ['0.875rem', '1.25rem'], // 14px
        lg: ['1rem', '1.5rem'],        // 16px
        xl: ['1.125rem', '1.5rem'],    // 18px
      },
      fontFamily: {
        // Optional: Set default font family
        sans: ["Space Mono", "system-ui"], // Example with Inter font
      },
      colors: {
        primary: {
          50: '#f8f9fa',
          100: '#f1f2f5',
          200: '#e3e5e8',
          300: '#d1d2d3',
          400: '#9da2a6',
          500: '#4a154b',
          600: '#350d36',
          700: '#2b092c',
          800: '#1e0e1e',
          900: '#0f0a0f',
        },
      },
    },
  },
  plugins: [],
} 