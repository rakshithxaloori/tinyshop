type OPTION_OBJECT = "option";

// Base interface for Option
interface OptionBase {
  name: string;
  values: string[] | null;
}

// Interface for OptionCreate
interface OptionCreate extends OptionBase {
  product: string;
}

// Interface for Option
interface Option extends OptionBase {
  id: string;
  object: OPTION_OBJECT;
}

// Interface for OptionList
interface OptionList {
  object: "list";
  url: "/v1/options";
  has_more: boolean;
  data: Option[];
}

// Interface for OptionUpdate
interface OptionUpdate {
  name?: string | null;
  values?: string[] | null;
}

// Interface for OptionDelete
interface OptionDelete {
  id: string;
  object: OPTION_OBJECT;
  deleted: boolean;
}

export type { Option, OptionCreate, OptionUpdate, OptionList, OptionDelete };
