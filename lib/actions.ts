'use server';

import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { EmotionLayoutStyles, EmotionLayoutStylesSchema } from '@/types/layout';

export type LayoutHistory = {
  messages: string[] | null;
  lastGeneratedObject: EmotionLayoutStyles | null;
}

export const generateProductLayoutObject = async (input: string,
  history?: LayoutHistory
) => {
  "use server";
  console.log('Generating product layout object with input:', input);
  let prompt;

  if (history) {
    if (history.messages) {
      prompt = `${prompt}\n\nHistory:\n${history.messages.join('\n')}`;
    }
    if (history.lastGeneratedObject) {
      prompt = `${prompt}\n\nLast generated object:\n${JSON.stringify(history.lastGeneratedObject, null, 2)}`;
    }
    prompt = `${prompt}\n\n Modify the exisiting product layout object with inline CSS style using the input : ${input}`
  } else {
    prompt = `Generate product layout object with inline CSS style using the input : ${input}`
  }

  const { object } = await generateObject({
    model: openai('gpt-4o-mini'),
    system: `You are a helpful assistant that generates inline style strings for product card layouts. 
    This will be used in conjunction with the css\`...\` function from @emotion/css to style product cards in a web application.
    For example:
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
    prompt,
    schema: EmotionLayoutStylesSchema,
    schemaName: 'EmotionLayoutStylesSchema',
    schemaDescription: EmotionLayoutStylesSchema.description,
  });


  return object;
}
