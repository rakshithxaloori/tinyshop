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
  object: typeof object_type.OPTION;
}

// Interface for OptionList
interface OptionList {
  object: "list";
  url: string;
  has_more: boolean;
  data: Option[] | null;
}

// Interface for OptionListQueryParams
interface OptionListQueryParams {
  product?: string;
}

// Interface for OptionUpdate
interface OptionUpdate {
  name?: string | null;
  values?: string[] | null;
}

// Interface for OptionDelete
interface OptionDelete {
  id: string;
  object: typeof object_type.OPTION;
  deleted: boolean;
}
