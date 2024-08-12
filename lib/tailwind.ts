import { twMerge } from 'tailwind-merge';
import { twi, twj } from 'tw-to-css';

const variants = ['hover', 'focus', 'active', 'disabled'];

export const tailwindToCSS = (tw: string) => {
  // there is a bug in the library which is causing "hover:bg-green-700 bg-orange-200" to return background-color: green; and not background-color: orange;
  const baseStyles = twj(tw);
  let variantStyles: Record<string, any> = {};

  // Extract variant styles
  variants.forEach(variant => {
    const variantClasses = tw.split(' ').filter(cls => cls.startsWith(`${variant}:`));
    if (variantClasses.length > 0) {
      const variantTw = variantClasses.map(cls => cls.replace(`${variant}:`, '')).join(' ');
      variantStyles[`&:${variant}`] = twj(variantTw);
    }
  });

  // Merge base styles with variant styles
  const mergedStyles = {
    ...baseStyles,
    ...variantStyles
  };

  console.log(mergedStyles);

  return mergedStyles;
}