'use server';

import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { ProductLayout, ProductLayoutSchema } from '@/components/structure/product';

export type LayoutHistory = {
  messages: string[] | null;
  lastGeneratedObject: ProductLayout | null;
}

const createPrompt = (input: string, history?: LayoutHistory, theme?: string) => {
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

  if (theme) {
    prompt = `${prompt}\n\n Respect daisy UI theme prop \"${theme}\"`
  }

  return prompt;
}

export const generateProductLayoutObject = async (input: string,
  history?: LayoutHistory, theme?: string
) => {
  "use server";
  console.log('Generating product layout object with input:', input);
  let prompt = createPrompt(input, history, theme);

  const { object } = await generateObject({
    model: openai('gpt-4o-mini'),
    system: `You are a helpful assistant that generates inline style strings for product card layouts. 
    This will be used in conjunction with the css\`...\` function from @emotion/css to style product cards in a web application.
    For example:
    {
      outerContainer: "background-color: white; border-radius: 8px; padding: 16px;",
      innerContainer: "display: flex; flex-direction: column;",
      imageContainer: "position: relative; overflow: hidden; aspect-ratio: 1;",
      image: "width: 100%; height: 100%; object-fit: cover;",
      wishlistContainer: "position: absolute; top: 0; right: 0; padding: 8px;",
      badge: "position: absolute; top: 0; left: 0; padding: 8px; border-radius: 9999px; background-color: red; color: white;",
      cardBodyContainer: "padding: 16px;",
      titleContainer: "",
      title: "font-size: 1.25rem; font-weight: 600;",
      priceContainer: "",
      price: "font-size: 1.25rem; font-weight: 600; color: green;",
      addToCartContainer: "display: flex; align-items: center; justify-content: space-between; margin-top: 16px;",
      addToCartButton: "padding: 8px 16px; border-radius: 8px; background-color: blue; color: white;",
      quantityContainer: "display: flex; align-items: center;",
      quantity: "margin: 0 8px; font-size: 1rem; font-weight: 600;",
      iconButtonContainer: "display: flex; align-items: center;",
      iconButton: "padding: 8px; border-radius: 9999px; background-color: blue; color: white;"
    }
    You can also use media queries, container queries and other CSS features to make the layout responsive and visually appealing.
    `,
    prompt,
    schema: ProductLayoutSchema,
    schemaName: 'ProductCardLayout',
    schemaDescription: ProductLayoutSchema.description,
  });


  return object;
}
