'use server';

import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { ProductLayout, ProductLayoutSchema } from '@/components/structure/product';
import { connectToDatabase, disconnectFromDatabase } from './mongo';

const MONGO_COLLECTION_NAME = process.env.MONGO_COLLECTION_NAME as string;

export type LayoutHistory = {
  messages: string[] | null;
  lastGeneratedObject: ProductLayout | null;
}

export type MongoLayoutInformation = {
  layout: ProductLayout;
  theme: string;
}

const createPrompt = (input: string, history?: LayoutHistory, theme?: string) => {
  let prompt;

  if (history && history?.messages) {
    if (history?.messages) {
      prompt = `${prompt}\n\nHistory of our conversation so far:\n${history.messages.join('\n')}`;
    }
    if (history?.lastGeneratedObject) {
      prompt = `${prompt}\n\nBased on the above conversations, last generated product layout object:\n${JSON.stringify(history.lastGeneratedObject, null, 2)}`;
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
    There are additional CSS classes from the daisyUI and tailwind CSS frameworks that can be used to style the product card.
    List of daisy UI theme variables are as follows:
    {
      "--p": "Primary color. Usage: background-color: oklch(var(--p)). Example value: 40.7232% 0.16116 17.530175",
      "--pc": "Foreground content color to use on primary color. Usage: color: oklch(var(--pc)). Example value: 88.1446% 0.032232 17.530175",
      "--s": "Secondary color. Usage: background-color: oklch(var(--s)). Example value: 61.6763% 0.169105 23.865865",
      "--sc": "Foreground content color to use on secondary color. Usage: color: oklch(var(--sc)). Example value: 12.3353% 0.033821 23.865865",
      "--a": "Accent color. Usage: background-color: oklch(var(--a)). Example value: 73.4253% 0.094994 60.729616",
      "--ac": "Foreground content color to use on accent color. Usage: color: oklch(var(--ac)). Example value: 14.6851% 0.018999 60.729616",
      "--n": "Neutral color. Usage: background-color: oklch(var(--n)). Example value: 54.3672% 0.037374 51.902819",
      "--nc": "Foreground content color to use on neutral color. Usage: color: oklch(var(--nc)). Example value: 90.8734% 0.007475 51.902819",
      "--b1": "Base color of page, used for blank backgrounds. Usage: background-color: oklch(var(--b1)). Example value: 95.8147% 0 0",
      "--b2": "Base color, a little darker. Usage: background-color: oklch(var(--b2)). Example value: 89.1077% 0 0",
      "--b3": "Base color, even more darker. Usage: background-color: oklch(var(--b3)). Example value: 82.4006% 0 0",
      "--bc": "Foreground content color to use on base color. Usage: color: oklch(var(--bc)). Example value: 19.1629% 0 0",
      "--in": "Info color. Usage: background-color: oklch(var(--in)). Example value: 69.2245% 0.097979 207.284192",
      "--inc": "Foreground content color to use on info color. Usage: color: oklch(var(--inc)). Example value: 13.8449% 0.019596 207.284192",
      "--su": "Success color. Usage: background-color: oklch(var(--su)). Example value: 60.9951% 0.080159 174.616213",
      "--suc": "Foreground content color to use on success color. Usage: color: oklch(var(--suc)). Example value: 12.199% 0.016032 174.616213",
      "--wa": "Warning color. Usage: background-color: oklch(var(--wa)). Example value: 70.0817% 0.164909 56.844303",
      "--wac": "Foreground content color to use on warning color. Usage: color: oklch(var(--wac)). Example value: 14.0163% 0.032982 56.844303",
      "--er": "Error color. Usage: background-color: oklch(var(--er)). Example value: 53.07% 0.241 24.16",
      "--erc": "Foreground content color to use on error color. Usage: color: oklch(var(--erc)). Example value: 90.614% 0.0482 24.16"
    }
    
    Sample output of the function should be an object of the following shape:
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
    You may choose to use the daisy UI theme variables to generate the background color, text color, border color, etc. But there is no compulsion on using the daisy UI theme variables.
    Decide what's best for the user experience and the design of the product card.
    `,
    prompt,
    schema: ProductLayoutSchema,
    schemaName: 'ProductCardLayout',
    schemaDescription: ProductLayoutSchema.description,
  });


  return object;
}

export const uploadLayoutInformationToMongo = async (object: MongoLayoutInformation) => {
  "use server";
  const { client, db } = await connectToDatabase();
  const collection = db.collection(MONGO_COLLECTION_NAME);

  // Create index for the collection, if it doesn't exist. create index on the shop field
  await collection.createIndex({ shop: 1, createdAt: -1 });

  const mongoObject = {
    ...object,
    createdAt: new Date(),
  };

  await collection.insertOne(mongoObject);
  await disconnectFromDatabase(client);
}