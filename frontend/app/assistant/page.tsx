"use client";

import { useEffect, useRef, useState } from "react";
import { ApiError, sendChatMessage } from "@/lib/api-client";
import { Panel } from "@/components/ui/Panel";
import { StatusPill } from "@/components/ui/StatusPill";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

type SendState = { phase: "idle" } | { phase: "sending" } | { phase: "error"; message: string };

const EXAMPLE_QUESTIONS = [
  "Produk apa yang perlu direstock?",
  "Berapa stok yang tersedia sekarang?",
  "Ada alert yang masih terbuka?",
];

export default function AssistantPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sendState, setSendState] = useState<SendState>({ phase: "idle" });
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sendState]);

  async function handleSend(question: string) {
    const trimmed = question.trim();
    if (!trimmed || sendState.phase === "sending") return;

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setSendState({ phase: "sending" });

    try {
      const response = await sendChatMessage(trimmed);
      setMessages((prev) => [...prev, { role: "assistant", content: response.answer }]);
      setSendState({ phase: "idle" });
    } catch (error) {
      setSendState({
        phase: "error",
        message: error instanceof ApiError ? error.message : "Unexpected error contacting the assistant.",
      });
    }
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    handleSend(input);
  }

  return (
    <div className="mx-auto max-w-3xl">
      <Panel eyebrow="AI · Assistant" title="Ask About Your Inventory">
        <div className="flex flex-col gap-4">
          {messages.length === 0 && (
            <div className="flex flex-col gap-3">
              <p className="text-text-secondary">
                Ask a question about current stock, restock recommendations, or open alerts.
              </p>
              <div className="flex flex-wrap gap-2">
                {EXAMPLE_QUESTIONS.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => handleSend(question)}
                    className="rounded border border-border px-3 py-1.5 text-sm text-text-secondary transition-colors hover:bg-surface-raised hover:text-text-primary"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div key={index} className="flex flex-col gap-1">
              <span className="font-mono text-[11px] uppercase tracking-wideish text-text-secondary">
                {message.role === "user" ? "You" : "Assistant"}
              </span>
              <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
            </div>
          ))}

          {sendState.phase === "sending" && (
            <div className="flex flex-col gap-1">
              <span className="font-mono text-[11px] uppercase tracking-wideish text-text-secondary">
                Assistant
              </span>
              <p className="text-sm text-text-secondary">Thinking…</p>
            </div>
          )}

          {sendState.phase === "error" && <StatusPill tone="critical">{sendState.message}</StatusPill>}

          <div ref={bottomRef} />
        </div>

        <form onSubmit={handleSubmit} className="mt-4 flex gap-2 border-t border-border pt-4">
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about stock levels, restocking, or alerts..."
            className="flex-1 rounded border border-border bg-surface-raised px-3 py-2 text-sm text-text-primary placeholder:text-text-secondary"
          />
          <button
            type="submit"
            disabled={sendState.phase === "sending" || !input.trim()}
            className="rounded bg-accent-muted px-4 py-2 text-sm font-medium text-accent transition-colors hover:bg-[rgba(62,217,196,0.24)] disabled:opacity-50"
          >
            Send
          </button>
        </form>
      </Panel>
    </div>
  );
}