"use client";

import { useEffect, useState } from "react";
import { ApiError, getHealth } from "@/lib/api-client";
import { Panel } from "@/components/ui/Panel";
import { StatusPill } from "@/components/ui/StatusPill";

type Probe =
  | { phase: "checking" }
  | { phase: "online"; status: string; timestamp: string; latencyMs: number }
  | { phase: "offline"; message: string };

const SHIPPED_MODULES = [
  {
    code: "IN",
    name: "Inventory Overview",
    description: "Current stock, safety stock, and restock status per product.",
    dependsOn: "GET /dashboard",
  },
  {
    code: "FC",
    name: "Forecast Visualization",
    description: "Predicted vs. actual demand per product, charted with Recharts.",
    dependsOn: "GET /products/{id}/forecasts",
  },
  {
    code: "AL",
    name: "Reorder & Alerts Panel",
    description: "Prioritized restock recommendations and the live alert feed.",
    dependsOn: "GET /dashboard",
  },
  {
    code: "AI",
    name: "Assistant",
    description: "Natural language Q&A over inventory metrics, grounded in live data.",
    dependsOn: "POST /chat",
  },
];

export default function HomePage() {
  const [probe, setProbe] = useState<Probe>({ phase: "checking" });
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    async function fetchHealth() {
      const start = performance.now();
      try {
        const health = await getHealth();
        if (!cancelled) {
          setProbe({
            phase: "online",
            status: health.status,
            timestamp: health.timestamp,
            latencyMs: Math.round(performance.now() - start),
          });
        }
      } catch (error) {
        if (!cancelled) {
          setProbe({
            phase: "offline",
            message: error instanceof ApiError ? error.message : "Unexpected error reaching the API.",
          });
        }
      }
    }

    fetchHealth();
    return () => {
      cancelled = true;
    };
  }, [refreshKey]);

  function handleRetry() {
    setProbe({ phase: "checking" });
    setRefreshKey((key) => key + 1);
  }

  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-6">
      <Panel eyebrow="System Manifest" title="Backend Connectivity">
        {probe.phase === "checking" && (
          <p className="text-text-secondary">Contacting the FastAPI backend&hellip;</p>
        )}

        {probe.phase === "online" && (
          <dl className="grid grid-cols-2 gap-4 sm:grid-cols-3">
            <div>
              <dt className="text-xs uppercase tracking-wideish text-text-secondary">Status</dt>
              <dd className="mt-1">
                <StatusPill tone="healthy">{probe.status}</StatusPill>
              </dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-wideish text-text-secondary">Latency</dt>
              <dd className="mt-1 font-data text-sm">{probe.latencyMs} ms</dd>
            </div>
            <div>
              <dt className="text-xs uppercase tracking-wideish text-text-secondary">
                Server time
              </dt>
              <dd className="mt-1 font-data text-sm">
                {new Date(probe.timestamp).toLocaleString()}
              </dd>
            </div>
          </dl>
        )}

        {probe.phase === "offline" && (
          <div className="flex items-start justify-between gap-4">
            <div>
              <StatusPill tone="critical">Unreachable</StatusPill>
              <p className="mt-2 text-sm text-text-secondary">{probe.message}</p>
              <p className="mt-1 text-sm text-text-secondary">
                Check that the API is running and that{" "}
                <code className="font-data">NEXT_PUBLIC_API_URL</code> points at it.
              </p>
            </div>
            <button
              onClick={handleRetry}
              className="shrink-0 rounded border border-border px-3 py-1.5 text-sm font-medium text-text-primary transition-colors hover:bg-surface-raised"
            >
              Retry
            </button>
          </div>
        )}
      </Panel>

      <Panel eyebrow="Sprint 04 · Build Manifest" title="Console Modules - Shipped">
        <ul className="divide-y divide-border">
          {SHIPPED_MODULES.map((mod) => (
            <li key={mod.code} className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
              <div className="flex items-start gap-3">
                <span className="mt-0.5 font-mono text-xs font-semibold tracking-wideish text-text-secondary">
                  {mod.code}
                </span>
                <div>
                  <p className="font-medium">{mod.name}</p>
                  <p className="text-sm text-text-secondary">{mod.description}</p>
                  <p className="mt-1 font-data text-xs text-text-secondary">
                    depends on <span className="text-accent">{mod.dependsOn}</span>
                  </p>
                </div>
              </div>
              <StatusPill tone="healthy">Live</StatusPill>
            </li>
          ))}
        </ul>
      </Panel>
    </div>
  );
}
