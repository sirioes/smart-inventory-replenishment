"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Bot, Boxes, LayoutGrid, LineChart, LogOut, type LucideIcon } from "lucide-react";
import { BellRing } from "lucide-react";

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

const NAV_ICONS: Record<string, LucideIcon> = {
  OV: LayoutGrid,
  IN: Boxes,
  FC: LineChart,
  AL: BellRing,
  AI: Bot,
};

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-border bg-surface text-text-primary">
      <div className="flex flex-col items-center gap-3 border-b border-border px-6 py-8">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-surface-raised font-display text-lg font-extrabold text-accent">
          SI
        </div>
        <div className="text-center leading-tight">
          <p className="font-display text-sm font-extrabold uppercase tracking-wideish">Smart Inventory</p>
          <p className="font-display text-sm font-extrabold uppercase tracking-wideish text-accent">
            Replenishment
          </p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <ul className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === "/" ? pathname === "/" : pathname?.startsWith(item.href);
            const Icon = NAV_ICONS[item.code];

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  aria-current={isActive ? "page" : undefined}
                  className={`flex items-center gap-3 rounded px-3 py-2.5 text-sm transition-colors ${
                    isActive
                      ? "bg-accent-muted text-accent"
                      : "text-text-secondary hover:bg-surface-raised hover:text-text-primary"
                  }`}
                >
                  {Icon && <Icon className="h-4 w-4 shrink-0" />}
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-border px-3 py-4">
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded px-3 py-2.5 text-sm text-text-secondary transition-colors hover:bg-surface-raised hover:text-text-primary"
        >
          <LogOut className="h-4 w-4 shrink-0" />
          <span className="font-medium">Logout</span>
        </button>
      </div>
    </aside>
  );
}
