import 'server-only';

import { MongoClient } from 'mongodb';

const MONGO_URI = process.env.MONGO_URI as string;
const MONGO_DB_NAME = process.env.MONGO_DB_NAME as string;

if (!MONGO_URI) {
  throw new Error('Please define the MONGO_URI environment variable');
}

if (!MONGO_DB_NAME) {
  throw new Error('Please define the MONGO_DB_NAME environment variable');
}


export async function connectToDatabase() {
  const client = await MongoClient.connect(MONGO_URI);
  const db = client.db(MONGO_DB_NAME);
  return { client, db };
}

export async function disconnectFromDatabase(client: MongoClient) {
  await client.close();
}