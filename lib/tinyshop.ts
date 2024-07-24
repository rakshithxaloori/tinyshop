import Tinyshop from "@tinyshop/tinyshop-node";

const secretKey = process.env.TINYSHOP_SECRET_KEY! as string
const apiHost = process.env.TINYSHOP_API_HOST! as string

export const tinyshop = new Tinyshop(secretKey, apiHost);