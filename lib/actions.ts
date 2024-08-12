'use server';

import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { LayoutClassesSchema } from '@/types/layout';

export const generateProductLayoutObject = async (input: string) => {
  "use server";
  const { object } = await generateObject({
    model: openai('gpt-4o-mini'),
    system: 'You are a helpful assistant that generates Tailwind CSS classes for product card layouts.',
    prompt: input,
    schema: LayoutClassesSchema,
    schemaName: 'LayoutClasses',
    schemaDescription: LayoutClassesSchema.description,
  });

  return object;
}
