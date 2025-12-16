module.exports = {
  content: [
    './core/templates/**/*.html',
    './accounts/templates/**/*.html',
    './orgs/templates/**/*.html'
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1e3a8a',
        secondary: '#2a4fc8'
      }
    }
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light']
  }
}
