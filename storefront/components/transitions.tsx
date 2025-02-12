"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useRouter } from "next/navigation";
import {
  createContext,
  MouseEventHandler,
  PropsWithChildren,
  use,
  useTransition,
} from "react";

export const DELAY = 200;

const sleep = (ms: number) =>
  new Promise<void>((resolve) => setTimeout(() => resolve(), ms));
const noop = () => { };

type TransitionContext = {
  pending: boolean;
  navigate: (url: string) => void;
};
const Context = createContext<TransitionContext>({
  pending: false,
  navigate: noop,
});
export const usePageTransition = () => use(Context);
export const usePageTransitionHandler = () => {
  const { navigate } = usePageTransition();
  const onClick: MouseEventHandler<HTMLAnchorElement> = (e) => {
    e.preventDefault();
    const href = e.currentTarget.getAttribute("href");
    if (href) navigate(href);
  };

  return onClick;
};

type Props = PropsWithChildren<{
  className?: string;
}>;

export default function Transitions({ children, className }: Props) {
  const [pending, start] = useTransition();
  const router = useRouter();
  const navigate = (href: string) => {
    start(async () => {
      router.push(href);
      await sleep(DELAY);
    });
  };

  const onClick: MouseEventHandler<HTMLDivElement> = (e) => {
    const a = (e.target as Element).closest("a");
    if (a) {
      e.preventDefault();
      const href = a.getAttribute("href");
      if (href) navigate(href);
    }
  };

  return (
    <Context.Provider value={{ pending, navigate }}>
      <div onClickCapture={onClick} className={className}>
        {children}
      </div>
    </Context.Provider>
  );
}

export function Animate({ children, className }: Props) {
  const { pending } = usePageTransition();
  const hidden = { opacity: 0 };
  const visible = { opacity: 1 };
  return (
    <AnimatePresence>
      {!pending && (
        <motion.div
          initial={hidden}
          animate={visible}
          exit={hidden}
          transition={{ duration: 0.200 }}
          className={className}
        >
          {children}
        </motion.div>
      )
      }
    </AnimatePresence >
  );
}

// https://github.com/shuding/next-view-transitions