type HeaderTitle = {
  name: string;
  image?: string | null;
}

type HeaderDropdownItem = {
  title: string;
  href: string;
  description?: string;
  image?: string | null;
}

type HeaderDropdown = {
  title: string;
  items: HeaderDropdownItem[];
}

type HeaderTemplate = {
  title: HeaderTitle;
  dropdown: HeaderDropdown[];
}