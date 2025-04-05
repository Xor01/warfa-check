export const fallbackLng = "en";
export const languages = [fallbackLng, "ar"];
export const defaultNS = "translation";
export const cookieName = "i18next";

export function getOptions(lng = fallbackLng, ns = defaultNS) {
  return {
    // debug: true,
    interpolation: {
      escapeValue: false,
    },
    supportedLngs: languages,
    fallbackLng,
    lng,
    fallbackNS: defaultNS,
    defaultNS,
    ns,
    removeLngFromUrl: true,
  };
}
