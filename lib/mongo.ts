"use server";

import { MongoClient } from 'mongodb';

const MONGO_URI = process.env.MONGO_URI as string;
const MONGO_DB_NAME = process.env.MONGO_DB_NAME as string;

if (!MONGO_URI) {
  throw new Error('Please define the MONGO_URI environment variable');
}

if (!MONGO_DB_NAME) {
  throw new Error('Please define the MONGO_DB_NAME environment variable');
}

let cachedClient: MongoClient | null = null;
let cachedDb: any = null;

export async function connectToDatabase() {
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  const client = await MongoClient.connect(MONGO_URI);

  const db = client.db(MONGO_DB_NAME);

  cachedClient = client;
  cachedDb = db;

  return { client, db };
}