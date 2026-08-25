"use client";

import { useEffect, useMemo, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ApiError, getDashboardData, getForecastHistory, getSalesHistory } from "@/lib/api-client";
import { Panel } from "@/components/ui/Panel";
import { StatusPill } from "@/components/ui/StatusPill";
import type { ProductDashboardItem } from "@/types/api";

type ProductsState =
  | { phase: "loading" }
  | { phase: "loaded"; products: ProductDashboardItem[] }
  | { phase: "error"; message: string };

type ChartState =
  | { phase: "idle" }
  | { phase: "loading" }
  | { phase: "loaded"; points: ChartPoint[] }
  | { phase: "error"; message: string };

interface ChartPoint {
  date: string;
  actual?: number;
  predicted?: number;
}

const AXIS_TICK_STYLE = { fontFamily: "var(--font-mono)", fontSize: 11, fill: "var(--text-secondary)" };

function mergeSeries(sales: { transaction_date: string; quantity_sold: number }[], forecasts: { forecast_date: string | null; predicted_demand: number }[]): ChartPoint[] {
  const byDate = new Map<string, ChartPoint>();

  for (const row of sales) {
    byDate.set(row.transaction_date, { date: row.transaction_date, actual: row.quantity_sold });
  }
  for (const row of forecasts) {
    if (!row.forecast_date) continue;
    const existing = byDate.get(row.forecast_date) ?? { date: row.forecast_date };
    existing.predicted = row.predicted_demand;
    byDate.set(row.forecast_date, existing);
  }

  return [...byDate.values()].sort((a, b) => a.date.localeCompare(b.date));
}

export default function ForecastsPage() {
  const [productsState, setProductsState] = useState<ProductsState>({ phase: "loading" });
  const [selectedProductId, setSelectedProductId] = useState<string | null>(null);
  const [chartState, setChartState] = useState<ChartState>({ phase: "idle" });

  useEffect(() => {
    let cancelled = false;

    async function fetchProducts() {
      try {
        const data = await getDashboardData();
        if (!cancelled) {
          setProductsState({ phase: "loaded", products: data.products });
          const firstProduct = data.products[0];
          if (firstProduct) {
            setSelectedProductId(firstProduct.product_id);
          }
        }
      } catch (error) {
        if (!cancelled) {
          setProductsState({
            phase: "error",
            message: error instanceof ApiError ? error.message : "Unexpected error loading products.",
          });
        }
      }
    }

    fetchProducts();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!selectedProductId) return;
    let cancelled = false;

    async function fetchChartData(productId: string) {
      setChartState({ phase: "loading" });
      try {
        const [sales, forecasts] = await Promise.all([
          getSalesHistory(productId),
          getForecastHistory(productId),
        ]);
        if (!cancelled) {
          setChartState({ phase: "loaded", points: mergeSeries(sales, forecasts) });
        }
      } catch (error) {
        if (!cancelled) {
          setChartState({
            phase: "error",
            message: error instanceof ApiError ? error.message : "Unexpected error loading chart data.",
          });
        }
      }
    }

    fetchChartData(selectedProductId);
    return () => {
      cancelled = true;
    };
  }, [selectedProductId]);

  const selectedProduct = useMemo(
    () =>
      productsState.phase === "loaded"
        ? productsState.products.find((p) => p.product_id === selectedProductId)
        : undefined,
    [productsState, selectedProductId],
  );

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <Panel eyebrow="FC · Forecasts" title="Predicted vs Actual Demand">
        {productsState.phase === "loading" && (
          <p className="text-text-secondary">Loading products…</p>
        )}

        {productsState.phase === "error" && (
          <StatusPill tone="critical">{productsState.message}</StatusPill>
        )}

        {productsState.phase === "loaded" && productsState.products.length === 0 && (
          <p className="text-text-secondary">No products found yet.</p>
        )}

        {productsState.phase === "loaded" && productsState.products.length > 0 && (
          <div className="flex flex-col gap-4">
            <label className="flex items-center gap-3 text-sm">
              <span className="text-text-secondary">Product</span>
              <select
                value={selectedProductId ?? ""}
                onChange={(event) => setSelectedProductId(event.target.value)}
                className="rounded border border-border bg-surface-raised px-3 py-1.5 font-data text-text-primary"
              >
                {productsState.products.map((product) => (
                  <option key={product.product_id} value={product.product_id}>
                    {product.sku} — {product.name}
                  </option>
                ))}
              </select>
              {selectedProduct && (
                <StatusPill tone={selectedProduct.needs_restock ? "critical" : "healthy"}>
                  {selectedProduct.needs_restock ? "Needs Restock" : "Healthy"}
                </StatusPill>
              )}
            </label>

            {chartState.phase === "loading" && (
              <p className="text-text-secondary">Loading chart data…</p>
            )}

            {chartState.phase === "error" && (
              <StatusPill tone="critical">{chartState.message}</StatusPill>
            )}

            {chartState.phase === "loaded" && chartState.points.length === 0 && (
              <p className="text-text-secondary">
                No sales or forecast history for this product yet.
              </p>
            )}

            {chartState.phase === "loaded" && chartState.points.length > 0 && (
              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartState.points}>
                    <CartesianGrid stroke="var(--border)" strokeDasharray="3 3" />
                    <XAxis dataKey="date" tick={AXIS_TICK_STYLE} stroke="var(--border)" />
                    <YAxis tick={AXIS_TICK_STYLE} stroke="var(--border)" />
                    <Tooltip
                      contentStyle={{
                        background: "var(--surface-raised)",
                        border: "1px solid var(--border)",
                        borderRadius: 6,
                        fontFamily: "var(--font-mono)",
                        fontSize: 12,
                      }}
                      labelStyle={{ color: "var(--text-primary)" }}
                    />
                    <Legend wrapperStyle={{ fontSize: 12, fontFamily: "var(--font-mono)" }} />
                    <Line
                      type="monotone"
                      dataKey="actual"
                      name="Actual sales"
                      stroke="var(--text-secondary)"
                      strokeWidth={2}
                      dot={false}
                      connectNulls
                    />
                    <Line
                      type="monotone"
                      dataKey="predicted"
                      name="Predicted demand"
                      stroke="var(--accent)"
                      strokeWidth={2}
                      dot={false}
                      connectNulls
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}
      </Panel>
    </div>
  );
}