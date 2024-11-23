/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#0088CC',
          dark: '#006699',
          light: '#33A3DA',
        },
        background: '#1C1C1E',
      },
    },
  },
  plugins: [],
  extend: {
    css: {
      '.swiper-pagination-bullet': {
        '@apply w-2 h-2 bg-white/50 opacity-100': {},
      },
      '.swiper-pagination-bullet-active': {
        '@apply bg-white': {},
      },
    },
  },
};
