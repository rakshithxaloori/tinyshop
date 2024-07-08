"use client";
import { SetStateAction, createContext, useState } from "react";


const PreviewContext = createContext(
  {
    preview: process.env.NEXT_PUBLIC_PREVIEW === "true",
    setPreview: (preview: boolean) => { },
    mode: "desktop",
    setMode: (mode: SetStateAction<string>) => { },
  }
);

const PreviewProvider = ({ children }
  : { children: React.ReactNode }
) => {
  const [preview, setPreview] = useState(process.env.NEXT_PUBLIC_PREVIEW === "true");
  const [mode, setMode] = useState("desktop");

  return (
    <PreviewContext.Provider value={{ preview, setPreview, mode, setMode }}>
      {children}
    </PreviewContext.Provider>
  );
}

export { PreviewContext, PreviewProvider };