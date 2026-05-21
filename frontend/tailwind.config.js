/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // warm theme: parchment-on-charcoal
        ink: "#1a1410",
        ink2: "#221a14",
        ink3: "#2c211a",
        paper: "#f5e9d3",
        ember: "#f59e0b",
        flame: "#ea580c",
        rose2: "#fb7185",
        sage: "#86efac",
        line: "#3a2e23",
      },
      fontFamily: {
        serif: ["Fraunces", "Georgia", "serif"],
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [],
};
