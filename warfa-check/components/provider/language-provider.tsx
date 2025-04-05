"use client";
import { createContext, useContext } from "react";

const LanguageContext = createContext<string | null>(null);

export default function LanguageProvider({
  children,
  lng,
}: {
  children: React.ReactNode;
  lng: string;
}) {
  return (
    <LanguageContext.Provider value={lng}>{children}</LanguageContext.Provider>
  );
}

export function useLanguage() {
  return useContext(LanguageContext);
}
