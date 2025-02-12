import * as React from "react"

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { PaletteIcon } from "lucide-react"

export function Themes({ selectedTheme, setSelectedTheme }: {
  selectedTheme: string;
  setSelectedTheme: (theme: string) => void;
}) {
  const themes = [
    { name: 'light', colors: ['#8b5cf6', '#ec4899', '#06b6d4', '#1f2937'] },
    { name: 'dark', colors: ['#9333ea', '#06b6d4', '#10b981', '#e5e7eb'] },
    { name: 'cupcake', colors: ['#65c3c8', '#ef9fbc', '#eeaf3a', '#291334'] },
    { name: 'bumblebee', colors: ['#fbbf24', '#fde68a', '#f59e0b', '#1f2937'] },
    { name: 'emerald', colors: ['#66cc8a', '#377cfb', '#f59e0b', '#1f2937'] },
    { name: 'corporate', colors: ['#4b6bfb', '#7b92b2', '#3abff8', '#1f2937'] },
    { name: 'synthwave', colors: ['#e779c1', '#f3cc30', '#d926a9', '#d926a9'] },
    { name: 'retro', colors: ['#e0a2ae', '#a7d3a6', '#b78468', '#2e282a'] },
    { name: 'cyberpunk', colors: ['#ff7598', '#75d1f0', '#ffd900', '#9d4edd'] },
    { name: 'valentine', colors: ['#e96d7b', '#a991f7', '#f2d5cf', '#632b3a'] },
    { name: 'halloween', colors: ['#f28c18', '#6d3a9c', '#51a800', '#ff7a00'] },
    { name: 'garden', colors: ['#5c7f67', '#e0e0e0', '#b1c77f', '#2b3a39'] },
    { name: 'forest', colors: ['#1eb854', '#c3e88d', '#82aaff', '#1a1b26'] },
    { name: 'aqua', colors: ['#07b9e9', '#3be1f0', '#0891b2', '#164e63'] },
    { name: 'lofi', colors: ['#808080', '#d9d9d9', '#4d4d4d', '#f2f2f2'] },
    { name: 'pastel', colors: ['#f5c6d6', '#d0e2ff', '#ffdab9', '#d8e2dc'] },
    { name: 'fantasy', colors: ['#f9d71c', '#e58e26', '#daa520', '#8b4513'] },
    { name: 'wireframe', colors: ['#b8b8b8', '#d9d9d9', '#737373', '#333333'] },
    { name: 'black', colors: ['#333333', '#666666', '#999999', '#cccccc'] },
    { name: 'luxury', colors: ['#d9d8c7', '#363636', '#804e00', '#b88b4a'] },
    { name: 'dracula', colors: ['#ff79c6', '#8be9fd', '#50fa7b', '#bd93f9'] },
    { name: 'cmyk', colors: ['#00bcd4', '#fdd835', '#e91e63', '#000000'] },
    { name: 'autumn', colors: ['#8c0327', '#ff8c00', '#ffd700', '#556b2f'] },
    { name: 'business', colors: ['#1c4e80', '#7a9e9f', '#4f6d7a', '#c0d6df'] },
    { name: 'acid', colors: ['#ff00ff', '#00ff00', '#ffff00', '#000000'] },
    { name: 'lemonade', colors: ['#ffff00', '#ffa500', '#00ff00', '#ffffff'] },
    { name: 'night', colors: ['#2a303c', '#3d4451', '#5c7f67', '#1fb2a5'] },
    { name: 'coffee', colors: ['#6f4e37', '#c0a080', '#dabb94', '#2c1d06'] },
    { name: 'winter', colors: ['#9ccaf8', '#ffffff', '#c9e3f8', '#0e3d6e'] },
    { name: 'dim', colors: ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6'] },
    { name: 'nord', colors: ['#5e81ac', '#81a1c1', '#88c0d0', '#8fbcbb'] },
    { name: 'sunset', colors: ['#ff7e5f', '#feb47b', '#ffb84d', '#f58634'] }
  ];

  return (
    <Select value={selectedTheme} onValueChange={setSelectedTheme} defaultValue="light">
      <SelectTrigger className="inline-flex shrink-0 items-center justify-center whitespace-nowrap text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-gray-100 gap-1 py-1 text-[#666666] hover:text-[#171717] px-2 h-8 w-auto rounded-md border bg-white ml-auto">
        <SelectValue className="w-lg" placeholder="Select a theme" asChild>
          <span >{selectedTheme}</span>
        </SelectValue>
        <PaletteIcon className="h-4 w-4" />
      </SelectTrigger>
      <SelectContent>
        <SelectGroup>
          <SelectLabel>Themes</SelectLabel>
          {themes.map((theme) => (
            <SelectItem
              key={theme.name}
              value={theme.name}
              className={`flex flex-row items-center justify-between`}
            >
              <span>{theme.name}</span>
              <div className="flex mt-1">
                {theme.colors.map((color, index) => (
                  <div
                    key={index}
                    className="w-3 h-3 rounded-full ml-1"
                    style={{ backgroundColor: color }}
                  />
                ))}
              </div>
            </SelectItem>
          ))}
        </SelectGroup>
      </SelectContent>
    </Select>
  )
}
