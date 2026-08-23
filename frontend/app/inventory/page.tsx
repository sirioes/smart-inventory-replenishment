import { EmptyState } from "@/components/ui/EmptyState";

export default function InventoryPage() {
  return (
    <EmptyState
      eyebrow="IN · Inventory"
      title="Inventory Overview"
      description="Every active product with current stock, safety stock, and restock status, sourced from GET /dashboard."
      issue="Inventory Overview & Product Status Page"
    />
  );
}
