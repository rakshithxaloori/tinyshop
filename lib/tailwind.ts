import { twi, twj } from 'tw-to-css';

const variants = ['hover', 'focus', 'active', 'disabled', 'dark',];

export const tailwindToCSS = (tw: string) => {
  // there is a bug in the library which is causing "hover:bg-green-700 bg-orange-200" to return background-color: green; and not background-color: orange;
  // filter out variants from the tailwind string

  const baseTw = tw.split(' ').filter(cls => !variants.some(variant => cls.startsWith(`${variant}:`))).join(' ');
  const baseStyles = twj(baseTw, {
    ignoreMediaQueries: false,
  });
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

  return mergedStyles;
}

export const tailwindToEmotionCSS = (tw: string) => {
  // there is a bug in the library which is causing "hover:bg-green-700 bg-orange-200" to return background-color: green; and not background-color: orange;
  // filter out variants from the tailwind string

  const baseTw = tw.split(' ').filter(cls => !variants.some(variant => cls.startsWith(`${variant}:`))).join(' ');
  const baseStyles = twi(baseTw, {
    ignoreMediaQueries: false,
  });
  let variantStyles: Record<string, any> = {};

  // Extract variant styles
  variants.forEach(variant => {
    const variantClasses = tw.split(' ').filter(cls => cls.startsWith(`${variant}:`));
    if (variantClasses.length > 0) {
      const variantTw = variantClasses.map(cls => cls.replace(`${variant}:`, '')).join(' ');
      variantStyles[`&:${variant}`] = `${twi(variantTw)}`;
    }
  });

  // return back a string composed of the base styles and the variant styles
  const variantStylesString = Object.entries(variantStyles).map(([key, value]) => `${key}: {${value}}`).join('; ');

  const emotionStyle = baseStyles + "\n" + variantStylesString;
  return emotionStyle;
}

// const tw = 'bg-green-700 hover:bg-orange-200 dark:bg-red-200  focus:bg-blue-200 active:bg-black disabled:bg-gray-200';
// console.log(tailwindToCSS(tw));

const tw2 = "text-sm text-gray-500 line-through";
// const twiStyle = twi(tw2);
// console.log(twiStyle);
// console.log(tailwindToCSS(tw2));
console.log(tailwindToEmotionCSS(tw2));