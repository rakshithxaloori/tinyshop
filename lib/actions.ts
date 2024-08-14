'use server';

import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { EmotionLayoutStylesSchema } from '@/types/layout';

export const generateProductLayoutObject = async (input: string) => {
  "use server";
  console.log('Generating product layout object with input:', input);

  const { object } = await generateObject({
    model: openai('gpt-4o-mini'),
    system: `You are a helpful assistant that generates Emotion class strings for product card layouts. For example:
    {
      container: "background-color: white; border-radius: 8px; padding: 16px;",
      image: "aspect-ratio: 1; object-fit: cover;",
      content: "padding: 16px;",
      title: "font-size: 1.25rem; font-weight: 600;",
      variant: "font-size: 1rem; font-weight: 400;",
      price: "font-size: 1.25rem; font-weight: 600; color: green;",
      compareAtPrice: "font-size: 1rem; text-decoration: line-through; color: gray;",
      badge: "font-size: 0.75rem; font-weight: 600; padding: 4px 8px; border-radius: 9999px; background-color: blue; color: white;"
    }
    You can also use media queries, container queries and other CSS features to make the layout responsive and visually appealing.
    `,
    prompt: input,
    schema: EmotionLayoutStylesSchema,
    schemaName: 'LayoutClasses',
    schemaDescription: EmotionLayoutStylesSchema.description,
  });

  return object;
}
