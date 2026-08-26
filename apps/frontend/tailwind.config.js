/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
        display: ['Poppins', 'sans-serif'],
        outfit: ['Outfit', 'sans-serif'],
      },
      colors: {
        primary: {
          DEFAULT: '#f62121',
          hover: '#d91c1c',
        },
        dark: {
          DEFAULT: '#0f172a',
          lighter: '#121e25',
          darker: '#0a0f1c'
        }
      }
    },
  },
  plugins: [],
}
