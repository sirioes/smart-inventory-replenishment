"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface NavItem {
  code: string;
  label: string;
  href: string;
}

export const NAV_ITEMS: NavItem[] = [
  { code: "OV", label: "Overview", href: "/" },
  { code: "IN", label: "Inventory", href: "/inventory" },
  { code: "FC", label: "Forecasts", href: "/forecasts" },
  { code: "AL", label: "Alerts", href: "/alerts" },
  { code: "AI", label: "Assistant", href: "/assistant" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-60 shrink-0 flex-col border-r border-border bg-surface">
      <div className="border-b border-border px-5 py-6">
        <p className="font-mono text-[11px] uppercase tracking-wideish text-accent">
          Stock Control
        </p>
        <h1 className="font-stencil text-3xl font-bold uppercase leading-[0.95] tracking-wideish">
          Smart Inventory
          <br />
          Replenishment
        </h1>
      </div>

      <nav className="flex-1 px-3 py-4">
        <ul className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === "/" ? pathname === "/" : pathname?.startsWith(item.href);

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  aria-current={isActive ? "page" : undefined}
                  className={`flex items-center gap-3 rounded px-3 py-2 text-sm transition-colors ${
                    isActive
                      ? "bg-accent-muted text-accent"
                      : "text-text-secondary hover:bg-surface-raised hover:text-text-primary"
                  }`}
                >
                  <span className="font-mono text-[11px] font-semibold tracking-wideish">
                    {item.code}
                  </span>
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-border px-5 py-4">
        <p className="font-mono text-[11px] uppercase tracking-wideish text-text-secondary">
          Sprint 04 · UI &amp; GenAI
        </p>
      </div>
    </aside>
  );
}
