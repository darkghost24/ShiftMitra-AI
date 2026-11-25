import React, { createContext, useContext, useState } from "react";
import { UI_STRINGS } from "../utils/translations";

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState("hi");

  const strings = UI_STRINGS[lang] || UI_STRINGS.hi;

  return (
    <LanguageContext.Provider value={{ lang, setLang, t: strings }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
