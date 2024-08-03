import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  // Get the current URL
  const url = new URL(req.url);

  // Get all query parameters
  const searchParams = url.searchParams;

  // Construct the new URL for redirection
  const redirectUrl = new URL("/thanks", url.origin);

  // Append all existing query parameters to the new URL
  searchParams.forEach((value, key) => {
    redirectUrl.searchParams.append(key, value);
  });

  // Redirect to the new URL using GET
  return NextResponse.redirect(redirectUrl.toString(), 303);
}