module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    "./public/**/*.html",
    './components/**/*.{js,ts,jsx,tsx}',
    './node_modules/@vercel/examples-ui/**/*.js',
    "./node_modules/flowbite-react/**/*.js",
  ],
  plugins: [
    require("flowbite/plugin")
  ],
  theme: {},
}
