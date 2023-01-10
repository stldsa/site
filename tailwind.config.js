/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.html"],
  theme: {
    colors: {
      'red': {
        DEFAULT: '#EC1F27',
        400: '#F04C53',
        300: '#F4797E',
        200: '#F7A5A9',
        100: '#FBD2D4'
      },
      'black': {
        DEFAULT: '#231F20',
        400: '#3B3838',
        300: '#605C5C',
        200: '#8C8989',
        100: '#C1C0BF'
      }
    },
    fontFamily: {

    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}
