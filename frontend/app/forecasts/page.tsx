import { EmptyState } from "@/components/ui/EmptyState";

export default function ForecastsPage() {
  return (
    <EmptyState
      eyebrow="FC · Forecasts"
      title="Forecast Visualization"
      description="Predicted vs. actual demand per product, charted with Recharts against forecast history."
      issue="Forecast Visualization Component"
    />
  );
}
