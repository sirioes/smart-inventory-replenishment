interface PanelProps {
  eyebrow?: string;
  title?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
}

export function Panel({ eyebrow, title, action, children, className = "" }: PanelProps) {
  return (
    <section className={`rounded border border-border bg-surface ${className}`}>
      {(eyebrow || title || action) && (
        <header className="flex items-center justify-between border-b border-border px-5 py-3">
          <div>
            {eyebrow && (
              <p className="font-mono text-[11px] uppercase tracking-wideish text-text-secondary">
                {eyebrow}
              </p>
            )}
            {title && <h2 className="font-display text-lg font-semibold leading-tight">{title}</h2>}
          </div>
          {action}
        </header>
      )}
      <div className="p-5">{children}</div>
    </section>
  );
}
