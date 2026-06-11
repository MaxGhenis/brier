import { redirect } from "next/navigation";

export default async function LegacyForecastRedirectPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  redirect(`/forecasts/${slug}`);
}
