import { z } from 'zod';

const LayoutClassesSchema = z.object({
  containerClass: z.string().describe("Tailwind classes for the main container of the product card"),
  imageClass: z.string().describe("Tailwind classes for the image container, try to use aspect-square for the image"),
  contentClass: z.string().describe("Tailwind classes for the content container (includes title, variant, price, etc.)"),
  titleClass: z.string().describe("Tailwind classes for the product title"),
  variantClass: z.string().describe("Tailwind classes for the product variant name"),
  priceClass: z.string().describe("Tailwind classes for the main price display"),
  compareAtPriceClass: z.string().describe("Tailwind classes for the compare-at price (usually styled as strikethrough)"),
  badgeClass: z.string().describe("Tailwind classes for the price type badge"),
}).describe("Layout classes for a product card using Tailwind CSS classes");

type LayoutClasses = z.infer<typeof LayoutClassesSchema>;

export type { LayoutClasses };

export { LayoutClassesSchema };