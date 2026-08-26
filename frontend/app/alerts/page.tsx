"use client";

import { useEffect, useState } from "react";
import { ApiError, getAlertsFeed, getDashboardData } from "@/lib/api-client";
import { Panel } from "@/components/ui/Panel";
import { StatusPill } from "@/components/ui/StatusPill";
import type { AlertFeedItem, ProductDashboardItem } from "@/types/api";

type RecommendationsState =
  | { phase: "loading" }
  | { phase: "loaded"; products: ProductDashboardItem[] }
  | { phase: "error"; message: string };

type AlertsState =
  | { phase: "loading" }
  | { phase: "loaded"; alerts: AlertFeedItem[] }
  | { phase: "error"; message: string };

function alertTone(status: string) {
  if (status === "open") return "critical" as const;
  if (status === "acknowledged") return "watch" as const;
  return "healthy" as const;
}

export default function AlertsPage() {
  const [recommendationsState, setRecommendationsState] = useState<RecommendationsState>({
    phase: "loading",
  });
  const [alertsState, setAlertsState] = useState<AlertsState>({ phase: "loading" });

  useEffect(() => {
    let cancelled = false;

    async function fetchRecommendations() {
      try {
        const data = await getDashboardData();
        if (!cancelled) {
          const needingRestock = data.products
            .filter((product) => product.needs_restock)
            .sort((a, b) => (b.recommended_qty ?? 0) - (a.recommended_qty ?? 0));
          setRecommendationsState({ phase: "loaded", products: needingRestock });
        }
      } catch (error) {
        if (!cancelled) {
          setRecommendationsState({
            phase: "error",
            message: error instanceof ApiError ? error.message : "Unexpected error loading recommendations.",
          });
        }
      }
    }

    fetchRecommendations();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    let cancelled = false;

    async function fetchAlerts() {
      try {
        const alerts = await getAlertsFeed();
        if (!cancelled) {
          setAlertsState({ phase: "loaded", alerts });
        }
      } catch (error) {
        if (!cancelled) {
          setAlertsState({
            phase: "error",
            message: error instanceof ApiError ? error.message : "Unexpected error loading alerts.",
          });
        }
      }
    }

    fetchAlerts();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6">
      <Panel eyebrow="AL · Reorder" title="Reorder Recommendations">
        {recommendationsState.phase === "loading" && (
          <p className="text-text-secondary">Loading recommendations…</p>
        )}

        {recommendationsState.phase === "error" && (
          <StatusPill tone="critical">{recommendationsState.message}</StatusPill>
        )}

        {recommendationsState.phase === "loaded" && recommendationsState.products.length === 0 && (
          <p className="text-text-secondary">No products currently need restocking.</p>
        )}

        {recommendationsState.phase === "loaded" && recommendationsState.products.length > 0 && (
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-border text-xs uppercase tracking-wideish text-text-secondary">
                <th className="pb-2 pr-4 font-medium">SKU</th>
                <th className="pb-2 pr-4 font-medium">Name</th>
                <th className="pb-2 pr-4 text-right font-medium">Current</th>
                <th className="pb-2 pr-4 text-right font-medium">Reorder Point</th>
                <th className="pb-2 text-right font-medium">Recommended Qty</th>
              </tr>
            </thead>
            <tbody>
              {recommendationsState.products.map((product) => (
                <tr key={product.product_id} className="border-b border-border last:border-0">
                  <td className="py-3 pr-4 font-data">{product.sku}</td>
                  <td className="py-3 pr-4">{product.name}</td>
                  <td className="py-3 pr-4 text-right font-data">{product.current_stock}</td>
                  <td className="py-3 pr-4 text-right font-data">{product.reorder_point ?? "—"}</td>
                  <td className="py-3 text-right font-data">{product.recommended_qty ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Panel>

      <Panel eyebrow="AL · Alerts" title="Alerts Feed">
        {alertsState.phase === "loading" && <p className="text-text-secondary">Loading alerts…</p>}

        {alertsState.phase === "error" && (
          <StatusPill tone="critical">{alertsState.message}</StatusPill>
        )}

        {alertsState.phase === "loaded" && alertsState.alerts.length === 0 && (
          <p className="text-text-secondary">No alerts yet.</p>
        )}

        {alertsState.phase === "loaded" && alertsState.alerts.length > 0 && (
          <ul className="divide-y divide-border">
            {alertsState.alerts.map((alert) => (
              <li key={alert.alert_id} className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
                <div>
                  <p className="font-medium">
                    {alert.sku} — {alert.name}
                  </p>
                  <p className="font-data text-xs text-text-secondary">
                    {alert.created_at} · {alert.channel} · qty {alert.recommended_qty}
                  </p>
                </div>
                <StatusPill tone={alertTone(alert.status)}>{alert.status}</StatusPill>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  );
}