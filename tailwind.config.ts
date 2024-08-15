import type { Config } from "tailwindcss"

const config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
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
      colors: {
        border: "hsl(var(--shadcn-border))",
        input: "hsl(var(--shadcn-input))",
        ring: "hsl(var(--shadcn-ring))",
        background: "hsl(var(--shadcn-background))",
        foreground: "hsl(var(--shadcn-foreground))",
        primary: {
          default: "hsl(var(--shadcn-primary))",
          foreground: "hsl(var(--shadcn-primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--shadcn-secondary))",
          foreground: "hsl(var(--shadcn-secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--shadcn-destructive))",
          foreground: "hsl(var(--shadcn-destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--shadcn-muted))",
          foreground: "hsl(var(--shadcn-muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--shadcn-accent))",
          foreground: "hsl(var(--shadcn-accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--shadcn-popover))",
          foreground: "hsl(var(--shadcn-popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--shadcn-card))",
          foreground: "hsl(var(--shadcn-card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--shadcn-radius)",
        md: "calc(var(--shadcn-radius) - 2px)",
        sm: "calc(var(--shadcn-radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
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
  plugins: [require("tailwindcss-animate"),
  require('daisyui'),

  ],
} satisfies Config

export default config