import { redirect } from "next/navigation";

export default function LegacyForecastsRedirectPage() {
  redirect("/forecasts");
}
