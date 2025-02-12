import { z } from 'zod';

const TailwindLayoutClassesSchema = z.object({
  containerClass: z.string().describe("Tailwind classes for the main container of the product card"),
  imageClass: z.string().describe("Tailwind classes for the image container, try to use aspect-square for the image"),
  contentClass: z.string().describe("Tailwind classes for the content container (includes title, variant, price, etc.)"),
  titleClass: z.string().describe("Tailwind classes for the product title"),
  variantClass: z.string().describe("Tailwind classes for the product variant name"),
  priceClass: z.string().describe("Tailwind classes for the main price display"),
  compareAtPriceClass: z.string().describe("Tailwind classes for the compare-at price (usually styled as strikethrough)"),
  badgeClass: z.string().describe("Tailwind classes for the price type badge"),
}).describe("Layout classes for a product card using Tailwind CSS classes");


const EmotionLayoutStylesSchema = z.object({
  container: z.string().describe(`Emotion CSS string for the main container of the product card. Ex: background-color: white; border-radius: 8px; padding: 16px;`),
  image: z.string().describe("Emotion CSS string for the image container, consider using aspect-ratio: 1 for square images. Ex: aspect-ratio: 1; object-fit: cover;"),
  content: z.string().describe("Emotion CSS string for the content container (includes title, variant, price, etc.). Ex: padding: 16px;"),
  title: z.string().describe("Emotion CSS string for the product title. Ex: font-size: 1.25rem; font-weight: 600;"),
  variant: z.string().describe("Emotion CSS string for the product variant name. Ex: font-size: 1rem; font-weight: 400;"),
  price: z.string().describe("Emotion CSS string for the main price display: Ex: font-size: 1.25rem; font-weight: 600; color: green;"),
  compareAtPrice: z.string().describe("Emotion CSS string for the compare-at price (usually styled with text-decoration: line-through). Ex: font-size: 1rem; text-decoration: line-through; color: gray;"),
  badge: z.string().describe("Emotion CSS string for the price type badge. Ex: font-size: 0.75rem; font-weight: 600; padding: 4px 8px; border-radius: 9999px; background-color: blue; color: white;"),
}).describe("Layout styles for a product card using inline style strings to be used as an input to css`` from @emotion/css");

type TailwindLayoutStyles = z.infer<typeof TailwindLayoutClassesSchema>;
type EmotionLayoutStyles = z.infer<typeof EmotionLayoutStylesSchema>;

export type { TailwindLayoutStyles, EmotionLayoutStyles };

export { TailwindLayoutClassesSchema, EmotionLayoutStylesSchema };