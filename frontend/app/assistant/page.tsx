import { EmptyState } from "@/components/ui/EmptyState";

export default function AssistantPage() {
  return (
    <EmptyState
      eyebrow="AI · Assistant"
      title="Inventory Assistant"
      description="Ask natural language questions about stock levels and restocking, answered by Llama 3.1 via Groq, grounded in real inventory data."
      issue="Frontend Chat Assistant Widget"
    />
  );
}
