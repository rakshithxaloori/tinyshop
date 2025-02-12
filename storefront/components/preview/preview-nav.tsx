"use client";

import { useContext, useState } from "react";
import { PreviewContext } from "./context";
import { Button } from "../ui/button";
import { LaptopMinimalIcon, SmartphoneIcon } from "lucide-react";

const PreviewNav = () => {
  const { preview, mode, setMode } = useContext(PreviewContext);
  const alertText = `Mode: ${mode === "desktop" ? "Desktop" : "Phone"}`
  if (!preview) return null;
  return (
    <div className="bg-primary flex flex-row p-2 px-10">
      {alertText}
      <div className="grow" />
      <label className="swap swap-rotate">
        {/* this hidden checkbox controls the state */}
        <input type="checkbox"
          className="hidden"
          checked={mode === "phone"}
          onChange={() =>
            setMode((currentMode: string) => currentMode === "desktop" ? "phone" : "desktop")
          }
        />

        {/* phone icon */}
        <SmartphoneIcon
          className="swap-on"
        />
        {/* desktop icon */}
        <LaptopMinimalIcon
          className="swap-off"
        />
      </label>
    </div>
  )
}

export default PreviewNav;
