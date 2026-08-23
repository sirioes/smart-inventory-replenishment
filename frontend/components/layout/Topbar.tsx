"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { getHealth } from "@/lib/api-client";
import { NAV_ITEMS } from "@/components/layout/Sidebar";
import { StatusPill } from "@/components/ui/StatusPill";

type ConnectionState =
  | { phase: "checking" }
  | { phase: "online"; timestamp: string }
  | { phase: "offline"; message: string };

export function Topbar() {
  const pathname = usePathname();
  const [connection, setConnection] = useState<ConnectionState>({ phase: "checking" });

  useEffect(() => {
    let cancelled = false;

    async function checkHealth() {
      try {
        const health = await getHealth();
        if (!cancelled) {
          setConnection({ phase: "online", timestamp: health.timestamp });
        }
      } catch (error) {
        if (!cancelled) {
          setConnection({
            phase: "offline",
            message: error instanceof Error ? error.message : "Unknown error",
          });
        }
      }
    }

    checkHealth();
    const interval = setInterval(checkHealth, 30_000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const activeItem =
    NAV_ITEMS.find((item) => (item.href === "/" ? pathname === "/" : pathname?.startsWith(item.href))) ??
    NAV_ITEMS[0];

  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-bg px-6">
      <div className="flex items-baseline gap-2">
        <span className="font-mono text-xs uppercase tracking-wideish text-text-secondary">
          {activeItem?.code}
        </span>
        <h2 className="font-display text-xl font-semibold uppercase tracking-wideish">
          {activeItem?.label}
        </h2>
      </div>

      {connection.phase === "checking" && <StatusPill tone="neutral">Checking API</StatusPill>}
      {connection.phase === "online" && <StatusPill tone="healthy">API Online</StatusPill>}
      {connection.phase === "offline" && (
        <StatusPill tone="critical">API Unreachable</StatusPill>
      )}
    </header>
  );
}
