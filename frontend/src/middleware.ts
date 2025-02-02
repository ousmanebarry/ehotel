import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  if (
    !request.nextUrl.pathname.match("/login") &&
    !request.nextUrl.pathname.match("/signup") &&
    !request.nextUrl.pathname.startsWith("/_next")
  ) {
    const access_token = request.cookies.get("access_token")?.value;

    if (!access_token) {
      return NextResponse.redirect(new URL("/login", request.url));
    }

    const role = request.cookies.get("role")?.value;

    if (
      role === "customer" &&
      request.nextUrl.pathname.startsWith("/employee")
    ) {
      return NextResponse.redirect(new URL("/", request.url));
    }
    if (
      role === "employee" &&
      !request.nextUrl.pathname.startsWith("/employee")
    ) {
      return NextResponse.redirect(new URL("/employee", request.url));
    }
  }

  if (
    request.nextUrl.pathname.match("/login") ||
    request.nextUrl.pathname.match("/signup")
  ) {
    const access_token = request.cookies.get("access_token")?.value;

    if (access_token) {
      const role = request.cookies.get("role")?.value;

      if (role == "employee") {
        return NextResponse.redirect(new URL("/employee", request.url));
      } else {
        return NextResponse.redirect(new URL("/", request.url));
      }
    }
  }
}
