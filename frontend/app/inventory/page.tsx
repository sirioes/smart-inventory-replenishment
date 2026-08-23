"use client";

import { useEffect, useState } from "react";
import { ApiError, getDashboardData } from "@/lib/api-client";
import { Panel } from "@/components/ui/Panel";
import { StatusPill } from "@/components/ui/StatusPill";
import type { ProductDashboardItem } from "@/types/api";

type LoadState =
  | { phase: "loading" }
  | { phase: "loaded"; products: ProductDashboardItem[] }
  | { phase: "error"; message: string };

const WATCH_MULTIPLIER = 1.2;

function statusFor(item: ProductDashboardItem) {
  if (item.reorder_point === null) {
    return { tone: "neutral" as const, label: "Not Evaluated", rank: 3 };
  }
  if (item.needs_restock) {
    return { tone: "critical" as const, label: "Needs Restock", rank: 0 };
  }
  if (item.current_stock <= item.reorder_point * WATCH_MULTIPLIER) {
    return { tone: "watch" as const, label: "Approaching", rank: 1 };
  }
  return { tone: "healthy" as const, label: "Healthy", rank: 2 };
}

export default function InventoryPage() {
  const [state, setState] = useState<LoadState>({ phase: "loading" });
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function fetchDashboard() {
      try {
        const data = await getDashboardData();
        if (!cancelled) {
          setState({ phase: "loaded", products: data.products });
        }
      } catch (error) {
        if (!cancelled) {
          setState({
            phase: "error",
            message:
              error instanceof ApiError ? error.message : "Unexpected error loading inventory.",
          });
        }
      }
    }

    fetchDashboard();
    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  function handleRetry() {
    setState({ phase: "loading" });
    setRefreshKey((key) => key + 1);
  }

  return (
    <div className="mx-auto max-w-5xl">
      <Panel eyebrow="IN · Inventory" title="Product Status">
        {state.phase === "loading" && <p className="text-text-secondary">Loading inventory…</p>}

        {state.phase === "error" && (
          <div className="flex items-start justify-between gap-4">
            <div>
              <StatusPill tone="critical">Failed to load</StatusPill>
              <p className="mt-2 text-sm text-text-secondary">{state.message}</p>
            </div>
            <button
              onClick={handleRetry}
              className="shrink-0 rounded border border-border px-3 py-1.5 text-sm font-medium text-text-primary transition-colors hover:bg-surface-raised"
            >
              Retry
            </button>
          </div>
        )}

        {state.phase === "loaded" && state.products.length === 0 && (
          <p className="text-text-secondary">No products found yet.</p>
        )}

        {state.phase === "loaded" && state.products.length > 0 && (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-border text-xs uppercase tracking-wideish text-text-secondary">
                <th className="pb-2 pr-4 font-medium">SKU</th>
                <th className="pb-2 pr-4 font-medium">Name</th>
                <th className="pb-2 pr-4 text-right font-medium">Current</th>
                <th className="pb-2 pr-4 text-right font-medium">Safety</th>
                <th className="pb-2 pr-4 text-right font-medium">Reorder Point</th>
                <th className="pb-2 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {[...state.products]
                .sort((a, b) => statusFor(a).rank - statusFor(b).rank)
                .map((product) => {
                  const status = statusFor(product);
                  return (
                    <tr key={product.product_id} className="border-b border-border last:border-0">
                      <td className="py-3 pr-4 font-data">{product.sku}</td>
                      <td className="py-3 pr-4">{product.name}</td>
                      <td className="py-3 pr-4 text-right font-data">{product.current_stock}</td>
                      <td className="py-3 pr-4 text-right font-data">{product.safety_stock}</td>
                      <td className="py-3 pr-4 text-right font-data">
                        {product.reorder_point ?? "—"}
                      </td>
                      <td className="py-3">
                        <StatusPill tone={status.tone}>{status.label}</StatusPill>
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        )}
      </Panel>
    </div>
  );
}