type Tone = "healthy" | "watch" | "critical" | "neutral" | "accent";

const TONE_STYLES: Record<Tone, string> = {
  healthy: "bg-healthy/15 text-healthy",
  watch: "bg-watch/15 text-watch",
  critical: "bg-critical/15 text-critical",
  neutral: "bg-text-secondary/15 text-text-secondary",
  accent: "bg-accent-muted text-accent",
};

const TONE_DOT: Record<Tone, string> = {
  healthy: "bg-healthy",
  watch: "bg-watch",
  critical: "bg-critical",
  neutral: "bg-text-secondary",
  accent: "bg-accent",
};

interface StatusPillProps {
  tone: Tone;
  children: React.ReactNode;
}

export function StatusPill({ tone, children }: StatusPillProps) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded px-2 py-0.5 text-xs font-medium uppercase tracking-wideish ${TONE_STYLES[tone]}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${TONE_DOT[tone]}`} aria-hidden />
      {children}
    </span>
  );
}
