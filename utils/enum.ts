const object_type = {
  PRODUCT: "product",
  OPTION: "option",
  VARIANT: "variant",
  PRICE: "price",
} as const;

type ObjectType = (typeof object_type)[keyof typeof object_type];

export { object_type };
export type { ObjectType };