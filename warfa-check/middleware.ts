import { NextResponse, NextRequest } from "next/server";
import acceptLanguage from "accept-language";
import { fallbackLng, languages } from "./i18n/settings";

acceptLanguage.languages(languages);

export default async function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  if (
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api") ||
    pathname.startsWith("/static") ||
    pathname.includes("/images/") ||
    pathname.endsWith(".ico") ||
    pathname.endsWith(".json") ||
    pathname.endsWith(".xml") ||
    pathname.endsWith(".txt")
  ) {
    return NextResponse.next();
  }

  if (
    pathname.startsWith(`/${fallbackLng}/`) ||
    pathname === `/${fallbackLng}`
  ) {
    return NextResponse.redirect(
      new URL(
        pathname.replace(
          `/${fallbackLng}`,
          pathname === `/${fallbackLng}` ? "/" : ""
        ),
        request.url
      )
    );
  }

  const pathnameIsMissingLocale = languages.every(
    (lang) => !pathname.startsWith(`/${lang}/`) && pathname !== `/${lang}`
  );

  let lang = fallbackLng;
  if (!pathnameIsMissingLocale) {
    const pathParts = pathname.split("/");
    if (pathParts.length > 1 && languages.includes(pathParts[1])) {
      lang = pathParts[1];
    }
  }

  // Create the response
  const response = pathnameIsMissingLocale
    ? NextResponse.rewrite(new URL(`/${fallbackLng}${pathname}`, request.url))
    : NextResponse.next();

  response.cookies.set("NEXT_LOCALE", lang, {
    path: "/",
    sameSite: "strict",
    maxAge: 60 * 60 * 24 * 30,
  });

  return response;
}

export const config = {
  matcher: [
    "/(.*)",
    "/((?!api|_next/static|_next/image|images).*)",
    "/((?!\\.json|\\.xml|\\.txt|\\.ico).*)",
  ],
};
