import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f5fbff',
          100: '#e0f2fe',
          500: '#0284c7',
          700: '#0369a1'
        }
      }
    }
  },
  plugins: []
};

export default config;
