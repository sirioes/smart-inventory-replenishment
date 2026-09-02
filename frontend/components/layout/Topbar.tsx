"use client";

import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { Bell, Search } from "lucide-react";
import { getHealth } from "@/lib/api-client";
import { NAV_ITEMS } from "@/components/layout/Sidebar";
import { StatusPill } from "@/components/ui/StatusPill";
import { ThemeToggle } from "@/components/ui/ThemeToggle";

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
    <header className="flex h-16 items-center justify-between gap-6 border-b border-border bg-surface px-6">
      <div className="flex items-baseline gap-2">
        <span className="font-mono text-xs uppercase tracking-wideish text-text-secondary">
          {activeItem?.code}
        </span>
        <h2 className="font-display text-xl font-semibold">{activeItem?.label}</h2>
      </div>

      <div className="flex flex-1 items-center justify-end gap-4">
        <label className="relative hidden max-w-xs flex-1 sm:block">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-secondary" />
          <input
            type="search"
            placeholder="Search"
            className="w-full rounded-full border border-border bg-surface-raised py-2 pl-9 pr-4 text-sm text-text-primary placeholder:text-text-secondary focus:outline-none"
          />
        </label>

        {connection.phase === "checking" && <StatusPill tone="neutral">Checking API</StatusPill>}
        {connection.phase === "online" && <StatusPill tone="healthy">API Online</StatusPill>}
        {connection.phase === "offline" && <StatusPill tone="critical">API Unreachable</StatusPill>}

        <ThemeToggle />

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-9 w-9 items-center justify-center rounded-full border border-border text-text-secondary transition-colors hover:bg-surface-raised hover:text-text-primary"
        >
          <Bell className="h-4 w-4" />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-critical" />
        </button>
      </div>
    </header>
  );
}
