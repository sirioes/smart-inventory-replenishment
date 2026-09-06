/** Round a raw model/calculation number to a whole unit for display. */
export function formatUnits(value: number | null | undefined): string {
  if (value == null) return "—";
  return String(Math.round(value));
}
