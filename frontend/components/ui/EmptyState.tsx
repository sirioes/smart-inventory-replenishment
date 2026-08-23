interface EmptyStateProps {
  eyebrow: string;
  title: string;
  description: string;
  issue: string;
}

export function EmptyState({ eyebrow, title, description, issue }: EmptyStateProps) {
  return (
    <div className="mx-auto flex max-w-lg flex-col items-start gap-3 rounded border border-dashed border-border p-8">
      <p className="font-mono text-xs uppercase tracking-wideish text-accent">{eyebrow}</p>
      <h2 className="font-display text-2xl font-semibold uppercase tracking-wideish">{title}</h2>
      <p className="text-text-secondary">{description}</p>
      <p className="font-data text-xs text-text-secondary">
        Ships in: <span className="text-text-primary">{issue}</span>
      </p>
    </div>
  );
}
