import Tinyshop from "@tinyshop/tinyshop-node";

const secretKey = process.env.TINYSHOP_SECRET_KEY! as string

export const tinyshop = new Tinyshop(secretKey);