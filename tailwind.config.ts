import type { Config } from "tailwindcss"
const {
  default: flattenColorPalette,
} = require("tailwindcss/lib/util/flattenColorPalette");


const config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
    './template/**/*.{ts,tsx}',
    './sections/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      margin: {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "2rem",
        "xl": "3.5rem",
        "2xl": "5.5rem",
      },
      padding: {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "2rem",
        "xl": "3.5rem",
        "2xl": "5.5rem",
      },
      animation: {
        "caret-blink": "caret-blink 1.25s ease-out infinite",
        buttonheartbeat: 'buttonheartbeat 1s infinite linear',
        'hover-pulse': 'hover-pulse 1s infinite ease-in-out',
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      keyframes: {
        "caret-blink": {
          "0%,70%,100%": { opacity: "1" },
          "20%,50%": { opacity: "0" },
        },
        'hover-pulse': {
          '0%': {
            boxShadow: '0 0 0 0 theme("colors.primary")'
          },
          '100%': {
            boxShadow: '0 0 0 1rem theme("colors.primary/0")'
          }
        },
        buttonheartbeat: {
          '0%': {
            'box-shadow': '0 0 0 0 theme("colors.primary")',
            transform: 'scale(0.98)',
          },
          '50%': {
            'box-shadow': '0 0 0 7px theme("colors.primary/0")',
            transform: 'scale(1)',
          },
          '100%': {
            'box-shadow': '0 0 0 0 theme("colors.primary/0")',
            transform: 'scale(0.98)',
          },
        },
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
    },
  },
  daisyui: {
    themes: true, // false: only light + dark | true: all themes | array: specific themes like this ["light", "dark", "cupcake"]
    darkTheme: "dark", // name of one of the included themes for dark mode
    base: true, // applies background color and foreground color for root element by default
    styled: true, // include daisyUI colors and design decisions for all components
    utils: true, // adds responsive and modifier utility classes
    prefix: "", // prefix for daisyUI classnames (components, modifiers and responsive class names. Not colors)
    logs: true, // Shows info about daisyUI version and used config in the console when building your CSS
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
  plugins: [
    require('tailwind-scrollbar-hide'),
    require('daisyui'),
    require("tailwindcss-animate"),
    // require('@tailwindcss/aspect-ratio'),
    addVariablesForColors,

  ],
} satisfies Config


// This plugin adds each Tailwind color as a global CSS variable, e.g. var(--gray-200).
function addVariablesForColors({ addBase, theme }: any) {
  let allColors = flattenColorPalette(theme("colors"));
  let newVars = Object.fromEntries(
    Object.entries(allColors).map(([key, val]) => [`--${key}`, val])
  );

  addBase({
    ":root": newVars,
  });
}

export default config

