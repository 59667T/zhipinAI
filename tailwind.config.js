/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  theme: {
    extend: {
      colors: {
        primary: '#165DFF',
        secondary: '#7B61FF',
        success: '#00B42A',
        warning: '#FF7D00',
        danger: '#F53F3F',
        neutral: '#F5F7FA'
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    }
  },
  plugins: [],
}
